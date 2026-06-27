# ================================================================================
# FamilyLife-style story event runtime split.
# Engine code lives in conditions.rpy, threads.rpy, and events.rpy.
# Authored thread definitions and event labels stay in StoryEventRuntime.rpy for now.
# ================================================================================

define amandaThreadList = [
    LThreadData(0, "amanda", "LegareDance", None, [
        amanda_dance_event("AmandaLegareDance_0", "story_amanda_legare_dance_0", "FridayDance", "enter", 0, "legare_intro", 0, "intro"),
        amanda_dance_event("AmandaLegareDance_1", "story_amanda_legare_dance_1", "FridayDance", "amanda_dance_legare", 1, "legare", 1, "talking"),
        amanda_dance_event("AmandaLegareDance_2", "story_amanda_legare_dance_2", "FridayDance", "amanda_dance_legare", 2, "legare", 2, "groping"),
        amanda_dance_event("AmandaLegareDance_3", "story_amanda_legare_dance_3", "FridayDance", "amanda_dance_legare", 3, "legare", 3, "kissing"),
        amanda_dance_event("AmandaLegareDance_4", "story_amanda_legare_dance_4", "FridayDance", "amanda_dance_legare", 4, "legare", 4, "after_dance"),
    ], highlight=False, threaded=True),
    LThreadData(0, "amanda", "FridayDanceMC", None, [
        amanda_dance_event("AmandaDance_0", "story_amanda_friday_dance_mc_0", "FridayDance", "amanda_dance_mc", 10, "mc", 0, "mc_dance", True),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "FridayDanceLegare", None, [
        amanda_dance_event("AmandaFridayDanceLegare_0", "story_amanda_friday_dance_legare_0", "FridayDance", "amanda_dance_legare", 20, "legare", 1, "talking", True),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "TavernSeductions", None, [
        (
            "story_amanda_tavern_seduction_0",
            (1, 2, 3, 4, 6), (12, 21), None,
            0.35,
            None,
            [
                "#amanda_tavern_seduction_ready()",
            ],
            None,
            "TavernMain",
            "enter",
            210,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "LizaWorkTalk", None, [
        (
            "story_amanda_liza_talk_work_0",
            (1, 2, 3, 4, 5, 6), (12, 17), None,
            1,
            None,
            [
                "#amanda_liza_talk_work_ready()",
            ],
            None,
            "TavernMain",
            "tavern_work",
            230,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "LizaGloryInvite", None, [
        (
            "story_amanda_liza_glory_invite_0",
            (1, 2, 3, 4, 6), (12, 21), None,
            1,
            None,
            [
                "#amanda_liza_glory_invite_ready()",
            ],
            None,
            "TavernMain",
            "enter",
            208,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "GloryAftermath", None, [
        (
            "story_amanda_glory_tavern_aftermath_0",
            (1, 2, 3, 4, 6), (12, 21), None,
            1,
            None,
            [
                "#amanda_glory_tavern_aftermath_ready()",
            ],
            None,
            "TavernMain",
            "enter",
            207,
        ),
        (
            "story_amanda_night_after_glory_0",
            None, (18, 23), None,
            1,
            None,
            [
                "#amanda_night_after_glory_ready()",
            ],
            None,
            "TavernAmandaRoom",
            "enter",
            20,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "TalkHub", None, [
        (
            "story_amanda_talk_hub_0",
            None, None, None,
            1,
            None,
            [
                "#amanda_talk_hub_ready()",
            ],
            None,
            "talk",
            "amanda",
            10,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "DressChange", None, [
        (
            "story_amanda_dress_change_0",
            None, None, None,
            1,
            None,
            [
                "#amanda_dress_change_thread_ready()",
            ],
            None,
            "talk_amanda",
            "dress_change",
            20,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "RoomNightApproach", None, [
        (
            "story_amanda_room_grope_0",
            None, (18, 23), None,
            1,
            None,
            [
                "#tavern_amanda_bed_action_available()",
            ],
            None,
            "TavernAmandaRoom",
            "amanda_grope",
            30,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "GloryHoleTry", None, [
        (
            "story_amanda_gloryhole_try_0",
            None, (12, 21), None,
            1,
            None,
            [
                "#amanda_gloryhole_try_ready()",
            ],
            None,
            "TavernGloryHole",
            "amanda_gloryhole_try",
            40,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "Birth", None, [
        (
            "story_amanda_give_birth_0",
            None, None, None,
            1,
            None,
            [
                "#amanda_birth_ready()",
            ],
            None,
            "TavernMain",
            "enter",
            7,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "LegareTavernVisits", None, [
        (
            "story_amanda_legare_tavern_visit_0",
            (1, 2, 3, 4, 6), (18, 21), None,
            0.5,
            None,
            [
                "#amanda_legare_tavern_visit_ready()",
            ],
            None,
            "TavernMain",
            "enter",
            205,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "StreetLegareSightings", None, [
        (
            "story_amanda_street_legare_sighting_0",
            (1, 2, 3, 4, 6), (12, 21), None,
            0.25,
            None,
            [
                "#amanda_street_legare_sighting_ready(CurLoc)",
            ],
            None,
            "StreetTavern",
            "enter",
            650,
        ),
        (
            "story_amanda_street_legare_sighting_0",
            (1, 2, 3, 4, 6), (12, 21), None,
            0.25,
            None,
            [
                "#amanda_street_legare_sighting_ready(CurLoc)",
            ],
            None,
            "MarketPlace",
            "enter",
            650,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "StreetLoverEncounters", None, [
        (
            "story_amanda_street_lover_encounter_0",
            (1, 2, 3, 4, 6), (12, 21), None,
            0.2,
            None,
            [
                "#amanda_street_lover_encounter_ready(CurLoc)",
            ],
            None,
            "StreetTavern",
            "enter",
            660,
        ),
        (
            "story_amanda_street_lover_encounter_0",
            (1, 2, 3, 4, 6), (12, 21), None,
            0.2,
            None,
            [
                "#amanda_street_lover_encounter_ready(CurLoc)",
            ],
            None,
            "MarketPlace",
            "enter",
            660,
        ),
    ], highlight=False, threaded=False),
]

define melissaThreadList = [
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
                "#int(Melissa.var.get('storage_rat_cleared', 0) or 0) == 0",
                "#str(getLocation('melissa') or '') == 'TavernStorage'",
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
    LThreadData(0, "melissa", "WerecatProblem", "melissaRatProblem_0", [
        (
            "story_melissa_werecat_rumor_0",
            None, None, None,
            1,
            None,
            [
                "#not (int(werecat_state().get('sold', 0) or 0) == 0 and int(werecat_state().get('adopted_count', 0) or 0) >= 1)",
                "#int(werecat_state().get('rats_problem_active', 0) or 0) == 1",
                "#int(Melissa.var.get('storage_rat_cleared', 0) or 0) == 1",
                "#int(Melissa.var.get('storage_rat_last_help_day', -1) or -1) >= 0",
                "#int(werecat_state().get('adopted', 0) or 0) == 0",
                "#int(werecat_state().get('sold', 0) or 0) == 0",
                "#int(werecat_state().get('hunter_tease_day', -1) or -1) < 0",
            ],
            None,
            "HunterClub",
            "overheard",
            0,
        ),
        (
            "story_melissa_werecat_intro_0",
            (1, 7), (6, 7), None,
            1,
            None,
            [
                "#int(werecat_state().get('rats_problem_active', 0) or 0) == 1",
                "#int(werecat_state().get('rat_breakfast_seen', 0) or 0) == 0",
                "#int(werecat_state().get('hunter_tease_day', -1) or -1) >= 0",
                "#not bool(BreakfastToday)",
            ],
            None,
            "TavernKitchen",
            "enter",
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
                "#not bool(BreakfastToday)",
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
                "#not bool(BreakfastToday)",
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
                "#int(Melissa.var.get('bats_episode', 0) or 0) <= 0",
                "#int(Melissa.var.get('storage_rat_last_help_day', -1) or -1) >= 0",
                "#calendar_v2.moon_phase_name_en(calendar_v2.day) == 'Full Moon'",
                "#not bool(BreakfastToday)",
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
            [
                "#int(Melissa.var.get('bats_episode', 0) or 0) == 1",
            ],
            None,
            "TavernUpstairs",
            "enter",
            1,
        ),
        (
            "story_melissa_bat_problem_2",
            None, None, None,
            1,
            None,
            [
                "#int(Melissa.var.get('bats_episode', 0) or 0) == 3",
                "#int(dayspassed or 0) >= int(Melissa.var.get('bat_attic_check_day', -1) or -1)",
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
            [
                "#int(Melissa.var.get('bats_episode', 0) or 0) in (4, 5)",
            ],
            None,
            "TavernAtic",
            "melissa_bats",
            3,
        ),
        (
            "story_melissa_bat_problem_5",
            None, None, None,
            1,
            None,
            [
                "#int(Melissa.var.get('bats_episode', 0) or 0) >= 6",
                "#int(Melissa.var.get('bats_episode', 0) or 0) < 8",
                "#str(Melissa.var.get('temp_room', '') or '') == 'TavernAmandaRoom'",
                "#int(Melissa.var.get('drawings_found', 0) or 0) == 0",
                "#int(dayspassed or 0) >= int(Melissa.var.get('drawings_ready_day', -1) or -1)",
            ],
            None,
            "TavernMelissaRoom",
            "room_search",
            4,
        ),
        (
            "story_melissa_bat_problem_4",
            None, None, None,
            1,
            None,
            [
                "#int(Melissa.var.get('bats_episode', 0) or 0) >= 6",
                "#int(Melissa.var.get('bats_episode', 0) or 0) < 8",
            ],
            None,
            "TavernAtic",
            "melissa_bats",
            5,
        ),
        (
            "story_melissa_bat_problem_6",
            None, None, None,
            1,
            None,
            [
                "#int(Melissa.var.get('bats_episode', 0) or 0) == 7",
                "#int(Melissa.var.get('roof_repair_complete_day', -1) or -1) >= 0",
                "#int(dayspassed or 0) >= int(Melissa.var.get('roof_repair_complete_day', -1) or -1)",
                "#int(Melissa.var.get('drawings_returned', 0) or 0) == 1",
            ],
            None,
            "TavernMain",
            "melissa_talk",
            6,
        ),
    ], highlight=False, threaded=True),
]

define sandraThreadList = [
    LThreadData(0, "sandra", "WeeklyEvaluation", None, [
        ("sandraWeeklyEvaluation_0", None, None, None, 1, None, ["#Sandra.weekly_thanks_event_ready()"], None, "TavernMyRoom", "sleep", 0),
        ("sandraWeeklyEvaluation_1", None, None, None, 1, None, ["#Sandra.weekly_thanks_event_ready()"], None, "TavernMyRoom", "sleep", 1),
        ("sandraWeeklyEvaluation_2", None, None, None, 1, None, ["#Sandra.weekly_thanks_event_ready()"], None, "TavernMyRoom", "sleep", 2),
        ("sandraWeeklyEvaluation_3", None, None, None, 1, None, ["#Sandra.weekly_thanks_event_ready()"], None, "TavernMyRoom", "sleep", 3),
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
                "#int(Clara.var.get('market_day_roll_day', -1) or -1) == int(dayspassed or 0)",
                "#int(Clara.var.get('market_day_roll', 0) or 0) == 1",
                "#int(Clara.var.get('booklet_market_seen', 0) or 0) == 0",
                "#not (int(Clara.var.get('market_follow_failed_day', -1) or -1) == int(dayspassed or 0) and int(Clara.var.get('market_follow_failed_hour', -1) or -1) == int(hour or 0))",
            ],
            None,
            "MarketPlace",
            "enter",
            0,
        ),
        (
            "story_clara_market_booklet_2",
            [1, 2, 3, 4, 6], (13, 15), None,
            1,
            None,
            [
                "#int(Clara.var.get('market_evening_roll_day', -1) or -1) == int(dayspassed or 0)",
                "#int(Clara.var.get('market_evening_roll', 0) or 0) == 1",
                "#int(Clara.var.get('booklet_market_seen', 0) or 0) == 1",
                "#int(Clara.var.get('market_evening_intro_seen', 0) or 0) == 0",
            ],
            None,
            "MarketPlace",
            "enter",
            1,
        ),
        (
            "story_clara_market_booklet_3",
            [1, 2, 3, 4, 6], (13, 15), None,
            1,
            None,
            [
                "#int(Clara.var.get('market_evening_roll_day', -1) or -1) == int(dayspassed or 0)",
                "#int(Clara.var.get('market_evening_roll', 0) or 0) == 1",
                "#int(Clara.var.get('market_evening_intro_seen', 0) or 0) == 1",
                "#int(Clara.var.get('mongol_theft_seen', 0) or 0) == 0",
            ],
            None,
            "MarketPlace",
            "enter",
            2,
        ),
        (
            "story_clara_market_booklet_4",
            None, None, None,
            1,
            None,
            [
                "#int(Clara.var.get('mongol_theft_seen', 0) or 0) == 1",
                "#int(Clara.var.get('escape_confessed', 0) or 0) == 0",
            ],
            None,
            "WineStore",
            "clara_talk",
            3,
        ),
        (
            "story_clara_market_booklet_5",
            None, None, None,
            1,
            None,
            [
                "#int(Clara.var.get('escape_confessed', 0) or 0) == 1",
                "#int(Mongol.var.get('StocksArrestDay', -1) or -1) < 0",
            ],
            None,
            "HunterClub",
            "overheard",
            4,
        ),
        (
            "story_clara_market_booklet_6",
            None, None, None,
            1,
            None,
            [
                "#int(Mongol.var.get('StocksArrestDay', -1) or -1) >= 0",
                "#int(Mongol.var.get('StocksSeen', 0) or 0) == 0",
            ],
            None,
            "CityGuard",
            "enter",
            5,
        ),
        (
            "story_clara_market_booklet_7",
            None, (16, 17), None,
            1,
            None,
            [
                "#int(Mongol.var.get('StocksSeen', 0) or 0) == 1",
                "#int(Mongol.var.get('StocksFoodDay', -1) or -1) < 0",
            ],
            None,
            "CityGuard",
            "enter",
            6,
        ),
        (
            "story_clara_market_booklet_8",
            (1, 6), (6, 12), None,
            1,
            None,
            [
                "#int(Mongol.var.get('StocksFoodDay', -1) or -1) >= 0",
                "#int(DraupnirVar.get('MongolLockpickOrderDay', -1) or -1) < 0",
            ],
            None,
            "StolyarWorkshop",
            "enter",
            7,
        ),
        (
            "story_clara_market_booklet_9",
            None, (16, 17), None,
            1,
            None,
            [
                "#int(DraupnirVar.get('MongolLockpickOrderDay', -1) or -1) >= 0",
                "#int(Mongol.var.get('StocksReleased', 0) or 0) == 0",
                "#int(dayspassed or 0) > int(Mongol.var.get('StocksFoodDay', -1) or -1)",
            ],
            None,
            "CityGuard",
            "enter",
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
                "#int(Melissa.var.get('drawings_found', 0) or 0) == 1",
                "#int(Clara.var.get('paintings_melissa_asked', 0) or 0) == 0",
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
                "#int(Clara.var.get('paintings_melissa_asked', 0) or 0) == 1",
                "#int(Clara.var.get('cellar_seen', 0) or 0) == 0",
                "#int(Clara.var.get('flirt', 0) or 0) > 0",
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
                "#int(Clara.var.get('comfort_pending', 0) or 0) == 1",
                "#int(Clara.var.get('comfort_done', 0) or 0) == 0",
                "#str(getLocation('clara') or '') == 'WineStore'",
            ],
            None,
            "WineStore",
            "clara_paintings",
            2,
        ),
        (
            "story_clara_paintings_second_ask_3",
            None, None, None,
            1,
            None,
            [
                "#int(Clara.var.get('second_ask_unlocked', 0) or 0) == 1",
                "#int(Clara.var.get('source_known', 0) or 0) == 0",
            ],
            None,
            "WineStore",
            "clara_paintings",
            3,
        ),
        (
            "story_clara_paintings_church_4",
            7, (6, 12), None,
            1,
            None,
            [
                "#int(Clara.var.get('source_known', 0) or 0) == 1",
                "#int(Clara.var.get('fiance_church_seen', 0) or 0) == 0",
            ],
            None,
            "Church",
            "clara_paintings",
            4,
        ),
        (
            "story_clara_paintings_barber_5",
            None, None, None,
            1,
            None,
            [
                "#int(Clara.var.get('fiance_church_seen', 0) or 0) == 1",
                "#int(Clara.var.get('fiance_barber_seen', 0) or 0) == 0",
                "#(8 <= int(hour or 0) <= 10 or ((int(hour or 0) >= 23 or int(hour or 0) <= 5) and int(Clara.var.get('fiance_barber_night_roll', 0) or 0) == 1))",
            ],
            None,
            "BarberShop",
            "clara_fiance",
            5,
        ),
        (
            "story_clara_paintings_commission_6",
            None, None, None,
            1,
            None,
            [
                "#int(Clara.var.get('fiance_barber_seen', 0) or 0) == 1",
                "#int(Clara.var.get('commission_started', 0) or 0) == 0",
                "#str(getLocation('clara') or '') == 'TavernMain'",
            ],
            None,
            "TavernMain",
            "clara_paintings",
            6,
        ),
        (
            "story_clara_paintings_commission_followup_7",
            None, (6, 7), None,
            1,
            None,
            [
                "#int(Clara.var.get('commission_started', 0) or 0) == 1",
                "#int(Clara.var.get('commission_followup_done', 0) or 0) == 0",
                "#int(dayspassed or 0) >= int(Clara.var.get('commission_followup_day', 999999) or 999999)",
                "#str(getLocation('clara') or '') == 'WineStore'",
            ],
            None,
            "WineStore",
            "clara_paintings",
            7,
        ),
        (
            "story_clara_paintings_evening_peek_8",
            None, (13, 15), None,
            1,
            None,
            [
                "#int(Clara.var.get('commission_followup_done', 0) or 0) == 1",
                "#int(Clara.var.get('peek_done', 0) or 0) == 0",
                "#str(getLocation('clara') or '') == 'WineStore'",
            ],
            None,
            "WineStore",
            "clara_paintings",
            8,
        ),
        (
            "story_clara_paintings_confession_9",
            None, None, None,
            1,
            None,
            [
                "#int(Clara.var.get('peek_done', 0) or 0) == 1",
                "#int(Clara.var.get('confession_done', 0) or 0) == 0",
                "#str(getLocation('clara') or '') == 'TavernMelissaRoom'",
                "#str(getLocation('melissa') or '') == 'TavernMelissaRoom'",
            ],
            None,
            "TavernMelissaRoom",
            "clara_paintings",
            9,
        ),
        (
            "story_clara_paintings_murder_10",
            None, None, None,
            1,
            None,
            [
                "#int(Clara.var.get('confession_done', 0) or 0) == 1",
                "#int(Clara.var.get('murder_seen', 0) or 0) == 0",
                "#int(dayspassed or 0) >= int(Clara.var.get('murder_day', 999999) or 999999)",
            ],
            None,
            "CityGuard",
            "enter",
            10,
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
                "#str(getLocation('clara') or '') == 'TavernMain'",
                "#str(getLocation('melissa') or '') == 'TavernMain'",
                "#int(Clara.var.get('tavern_visit_bar_0_seen', 0) or 0) == 0",
                "#not household_runtime_event_seen_today('clara_tavern_visit')",
            ],
            None,
            "TavernMain",
            "clara_tavern_visit",
            0,
        ),
        (
            "story_clara_tavern_visit_bar_1",
            [1, 2, 3, 4, 5, 6], (12, 17), None,
            1,
            None,
            [
                "#str(getLocation('clara') or '') == 'TavernMain'",
                "#str(getLocation('melissa') or '') == 'TavernMain'",
                "#int(Clara.var.get('tavern_visit_bar_0_seen', 0) or 0) == 1",
                "#int(Clara.var.get('tavern_visit_bar_1_seen', 0) or 0) == 0",
                "#Amanda.var_int('attic_window_busted', 0) == 1",
                "#int(Melissa.var.get('bats_episode', 0) or 0) >= 6",
                "#not household_runtime_event_seen_today('clara_tavern_visit')",
            ],
            None,
            "TavernMain",
            "clara_tavern_visit",
            1,
        ),
        (
            "story_clara_tavern_visit_bar_2",
            [1, 2, 3, 4, 5, 6], (18, 22), None,
            1,
            None,
            [
                "#str(getLocation('clara') or '') == 'TavernMain'",
                "#str(getLocation('melissa') or '') == 'TavernMain'",
                "#int(Clara.var.get('tavern_visit_bar_1_seen', 0) or 0) == 1",
                "#int(Clara.var.get('tavern_visit_bar_2_seen', 0) or 0) == 0",
                "#int(Melissa.var.get('drawings_booklet_read', 0) or 0) == 1 or int(Melissa.var.get('drawings_booklet_left', 0) or 0) == 1",
                "#not household_runtime_event_seen_today('clara_tavern_visit')",
            ],
            None,
            "TavernMain",
            "clara_tavern_visit",
            2,
        ),
        (
            "story_clara_melissa_room_visit_0",
            None, (16, 22), None,
            1,
            None,
            [
                "#str(getLocation('clara') or '') == 'TavernMelissaRoom'",
                "#str(getLocation('melissa') or '') == 'TavernMelissaRoom'",
                "#int(Melissa.var.get('bats_episode', 0) or 0) >= 8",
                "#int(Melissa.var.get('drawings_found', 0) or 0) == 1",
                "#int(Clara.var.get('melissa_room_visit_0_seen', 0) or 0) == 0",
                "#not household_runtime_event_seen_today('clara_melissa_room_visit')",
            ],
            None,
            "TavernMelissaRoom",
            "clara_room_visit",
            3,
        ),
        (
            "story_clara_melissa_room_visit_1",
            None, (16, 22), None,
            1,
            None,
            [
                "#str(getLocation('clara') or '') == 'TavernMelissaRoom'",
                "#str(getLocation('melissa') or '') == 'TavernMelissaRoom'",
                "#int(Melissa.var.get('bats_episode', 0) or 0) >= 8",
                "#int(Clara.var.get('melissa_room_visit_0_seen', 0) or 0) == 1",
                "#int(Clara.var.get('melissa_room_visit_1_seen', 0) or 0) == 0",
                "#not household_runtime_event_seen_today('clara_melissa_room_visit')",
            ],
            None,
            "TavernMelissaRoom",
            "clara_room_visit",
            4,
        ),
        (
            "story_clara_melissa_room_visit_2",
            None, (16, 22), None,
            1,
            None,
            [
                "#str(getLocation('clara') or '') == 'TavernMelissaRoom'",
                "#str(getLocation('melissa') or '') == 'TavernMelissaRoom'",
                "#int(Melissa.var.get('bats_episode', 0) or 0) >= 8",
                "#int(Clara.var.get('melissa_room_visit_1_seen', 0) or 0) == 1",
                "#int(Clara.var.get('melissa_room_visit_2_seen', 0) or 0) == 0",
                "#not household_runtime_event_seen_today('clara_melissa_room_visit')",
            ],
            None,
            "TavernMelissaRoom",
            "clara_room_visit",
            5,
        ),
    ], highlight=False, threaded=True),
]
define beckyThreadList = [
    LThreadData(0, "becky", "FridayDanceMC", None, [
        becky_dance_event("BeckyDance_0", "story_becky_friday_dance_mc_0", "FridayDance", "becky_dance_mc", 10, "mc", 0, "mc_dance", True),
    ], highlight=False, threaded=False),
    LThreadData(0, "becky", "IngaFirstTalk", None, [
        ("story_becky_talk_inga_0", None, None, None, 1, None, [
            "#Becky.var.get('SawIngaFuck', 0) == 1",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_inga1", 10),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "IngaSecondTalk", None, [
        ("story_becky_talk_inga_1", None, None, None, 1, None, [
            "#Becky.var.get('SawIngaFuck', 0) == 2",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_inga2", 20),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "LucasTalk", None, [
        ("story_becky_talk_lucas_0", None, None, None, 1, None, [
            "#Becky.var.get('SawIngaFuck', 0) == 3",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_lucas", 30),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "HusbandFirstTalk", None, [
        ("story_becky_talk_husband_0", None, None, None, 1, None, [
            "#Becky.var.get('husbandtalk', 0) == 1",
            "#Becky.rel > 13",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_husband1", 40),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "HusbandSecondTalk", None, [
        ("story_becky_talk_husband_1", None, None, None, 1, None, [
            "#Becky.var.get('husbandtalk', 0) == 2",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_husband2", 50),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "HusbandThirdTalk", None, [
        ("story_becky_talk_husband_2", None, None, None, 1, None, [
            "#Becky.var.get('husbandtalk', 0) == 3",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_husband3", 60),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "HusbandFourthTalk", None, [
        ("story_becky_talk_husband_3", None, None, None, 1, None, [
            "#Becky.var.get('husbandtalk', 0) == 4",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_husband4", 70),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "EddieFirstTalk", None, [
        ("story_becky_talk_eddie_0", None, None, None, 1, None, [
            "#Becky.var.get('eddietalk', 0) == 0",
            "#Becky.rel > 6",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_eddie1", 80),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "EddieGeorgettTalk", None, [
        ("story_becky_talk_eddie_georgett_0", None, None, None, 1, None, [
            "#int(Eddie.var.get('TalkedAboutGeorgett', 0) or 0) > 0",
            "#Becky.var.get('husbandtalk', 0) > 0",
            "#Becky.var.get('eddietalk', 0) > 0",
            "#Becky.rel > 8",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_eddie2", 90),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "HomeInviteTalk", None, [
        ("story_becky_home_invite_talk_0", None, None, None, 1, None, [
            "#Becky.var.get('visitedhome', 0) == 2",
            "#Becky.rel > 12",
            "#Becky.talk_count() < 2",
            "#str(player_state().appearance.current_dress or '') == 'citydress'",
            "#int(charisma or 0) > 75",
        ], None, "talk_becky", "becky_talk_invite", 100),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "HomeLastVisitTalk", None, [
        ("story_becky_home_last_visit_talk_0", None, None, None, 1, None, [
            "#Becky.var.get('TimesVisited', 0) > 0",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_lastvisit", 110),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "EddieBehaviorTalk", None, [
        ("story_becky_talk_eddie_behavior_0", None, None, None, 1, None, [
            "#Becky.var.get('visitedhome', 0) >= 3",
            "#int(Eddie.var.get('SawMomSex', 0) or 0) > 0 or Becky.var.get('HomeSex', 0) > 0",
            "#Becky.var.get('visitedhome', 0) < 7",
            "#Becky.var.get('EddieTryToFuck', 0) < 4",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_eddie3", 120),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "EddieGeorgMentionTalk", None, [
        ("story_becky_talk_eddie_georgett_1", None, None, None, 1, None, [
            "#Becky.var.get('EddieGeorg', 0) > 1",
            "#Becky.var.get('visitedhome', 0) < 7",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_eddie4", 130),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "EddieReactionTalk", None, [
        ("story_becky_talk_eddie_reaction_0", None, None, None, 1, None, [
            "#Becky.var.get('GeorgMention', 0) == 1",
            "#Becky.var.get('visitedhome', 0) < 7",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_eddie5", 140),
        ("story_becky_talk_eddie_reaction_1", None, None, None, 1, None, [
            "#Becky.var.get('GeorgMention', 0) == 1",
            "#Becky.var.get('visitedhome', 0) < 7",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_eddie6", 141),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "EddieAfterSexTalk", None, [
        ("story_becky_talk_eddie_after_sex_0", None, None, None, 1, None, [
            "#(Becky.var.get('EddieTryToFuck', 0) == 4 and Becky.var.get('AskedEddieFuck', 0) == 0) or (Becky.var.get('visitedhome', 0) >= 7 and Becky.var.get('AskedEddieFuck', 0) < 2)",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_eddie7", 150),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "PregnancyFatherTalk", None, [
        ("story_becky_talk_pregnancy_0", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
            "#Becky.rel >= 8",
            "#int(Becky.stats.get('pregnancy', 0) or 0) >= 120",
            "#str(DaddyAskBuildPhrase('becky') or '') != ''",
        ], None, "talk_becky", "becky_talk_pregnancy", 160),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "SherwoodOfferTalk", None, [
        ("story_becky_sherwood_offer_0", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
            "#Becky.var.get('TradeOffer', 0) == 2",
        ], None, "talk_becky", "becky_talk_sherwood_offer", 170),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "SherwoodElvesTalk", None, [
        ("story_becky_sherwood_elves_0", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
            "#Becky.var.get('TradeOffer', 0) == 1",
            "#Becky.var.get('AskTradeElf', 0) == 0",
        ], None, "talk_becky", "becky_talk_sherwood_elves", 171),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "SherwoodFingalTalk", None, [
        ("story_becky_sherwood_fingal_0", None, None, None, 1, None, [
            "#Becky.var.get('TradeOffer', 0) == 1",
            "#int(Eddie.var.get('FingalTalk', 0) or 0) > 0",
            "#Becky.var.get('FingalClarify', 0) == 0",
            "#Becky.var.get('AdmitSherwood', 0) == 0",
        ], None, "talk_becky", "becky_talk_sherwood_fingal", 172),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "SherwoodWarnTalk", None, [
        ("story_becky_sherwood_warn_0", None, None, None, 1, None, [
            "#Becky.var.get('TradeOffer', 0) == 1",
            "#Becky.var.get('SherwoodWarn', 0) == 1",
            "#Becky.var.get('AdmitSherwood', 0) == 0",
        ], None, "talk_becky", "becky_talk_sherwood_warn", 173),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "SherwoodRoadTalk", None, [
        ("story_becky_sherwood_road_0", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
            "#Becky.var.get('TradeOffer', 0) == 1",
            "#Becky.var.get('AdmitSherwood', 0) == 0",
            "#Becky.var.get('KnowSherwood', 0) == 1",
        ], None, "talk_becky", "becky_talk_sherwood_road", 174),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "SherwoodLiedTalk", None, [
        ("story_becky_sherwood_lied_0", None, None, None, 1, None, [
            "#Becky.var.get('TradeOffer', 0) == 1",
            "#Becky.var.get('AdmitSherwood', 0) == 1",
        ], None, "talk_becky", "becky_talk_sherwood_lied", 175),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "SherwoodRobbedTalk", None, [
        ("story_becky_sherwood_robbed_0", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
            "#Becky.var.get('RobbedByRobin', 0) == 1",
        ], None, "talk_becky", "becky_talk_sherwood_robbed", 176),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "SherwoodHowToTalk", None, [
        ("story_becky_sherwood_howto_0", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
            "#Becky.var.get('ConsoleRobbery', 0) == 0",
            "#Becky.var.get('RobbedByRobin', 0) >= 2",
        ], None, "talk_becky", "becky_talk_sherwood_howto", 177),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "SherwoodWarnedTalk", None, [
        ("story_becky_sherwood_warned_0", None, None, None, 1, None, [
            "#Becky.var.get('RobbedByRobin', 0) == 2",
            "#Becky.var.get('AdmitSherwood', 0) == 0",
        ], None, "talk_becky", "becky_talk_sherwood_warned", 178),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "HomeFrontIngaLucas", None, [
        ("story_becky_home_front_inga_0", None, None, None, 1, None, [
            "#int(Becky.var.get('HomeFrontCheckedDay', -1) or -1) != int(dayspassed or 0)",
            "#int(Becky.var.get('TodayFrontSexCheck', 0) or 0) == 0",
        ], None, "BeckyHomeFront", "enter", 300),
    ], highlight=False, threaded=False),
    LThreadData(0, "becky", "HomeVisitEntry", None, [
        ("story_becky_home_visit_0", None, None, None, 1, None, [
            "#str(ArriveMode or '') == ''",
            "#int(Becky.var.get('HomeEnterCheckedDay', -1) or -1) != int(dayspassed or 0)",
        ], None, "BeckyHome", "enter", 310),
    ], highlight=False, threaded=False),
    LThreadData(0, "becky", "HomeDanceArrival", None, [
        ("story_becky_home_from_dances_0", None, None, None, 1, None, [
            "#str(ArriveMode or '') == 'FromDances'",
            "#int(Becky.var.get('visitedhome', 0) or 0) < 5",
        ], None, "BeckyHome", "enter", 320),
    ], highlight=False, threaded=False),
    LThreadData(0, "becky", "HomeDinnerBedroom", None, [
        ("story_becky_home_from_dinner_0", None, None, None, 1, None, [
            "#str(ArriveMode or '') == 'FromDinner'",
        ], None, "BeckyHome", "enter", 330),
    ], highlight=False, threaded=False),
    LThreadData(0, "becky", "HomeEddieBedroom", None, [
        ("story_becky_home_svalnyi_greh_0", None, None, None, 1, None, [
            "#str(ArriveMode or '') == 'SvalnyiGreh'",
        ], None, "BeckyHome", "enter", 340),
    ], highlight=False, threaded=False),
    LThreadData(0, "becky", "GeorgettHomeVisit", None, [
        (
            "GeorgettBeckyVisit",
            None, (18, 23), None,
            1,
            None,
            [
                "#int(Becky.var.get('EddieWhoreHome', 0) or 0) == 4",
                "#int(Becky.var.get('visitedhome', 0) or 0) >= 5",
                "#int(Becky.var.get('HomeSex', 0) or 0) > 0",
                "#int(Eddie.var.get('SawMomSex', 0) or 0) > 0",
                "#CheckIfSexEventExist('georgett', 99, 'EddieHomeVisit') > 0",
            ],
            None,
            "BeckyHome",
            "georgett_home_visit",
            350,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "becky", "ChurchAfterSermon", None, [
        (
            "story_becky_church_after_sermon",
            7, (11, 12), None,
            1,
            None,
            [
                "#church_after_cermon_action_visible()",
                "#int(Becky.var.get('PriestAdvice', 0) or 0) > 0",
                "#Becky.after_sermon_stage() < 4",
                "#CheckIfSexEventExist('becky', 99, 'Priest') > 0",
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
                "#int(Becky.var.get('TradeOffer', 0) or 0) == 1",
                "#str(CurLoc or '') == 'BlackwoodRoad'",
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
    RThreadData(0, "tavern", "WorkRandomEvents", None, [1, [
        # (target, day, hour, delay, probability, reqs, condition, item, location, action, priority)
        (
            "TavernWorkEventTrigger", None, None, None,
            1,
            None,
            [
                "#tavern_work_planned_for('WaitressHarass', CurLoc, time)",
            ],
            None,
            "TavernMain",
            "tavern_work",
            200,
        ),
        (
            "TavernWorkEventTrigger", None, None, None,
            1,
            None,
            [
                "#tavern_work_planned_for('CleaningHarass', CurLoc, time)",
            ],
            None,
            "TavernMain",
            "tavern_work",
            210,
        ),
        (
            "TavernWorkEventTrigger", None, None, None,
            1,
            None,
            [
                "#tavern_work_planned_for('FightSmall', CurLoc, time)",
            ],
            None,
            "TavernMain",
            "tavern_work",
            220,
        ),
    ]], highlight=False, threaded=False),
]
define cityThreadList = [
    RThreadData(0, "city", "StreetChronicles", None, [1, [
        # (target, day, hour, delay, probability, reqs, condition, item, location, action, priority)
        (
            "TownStreetPatrolEvent", None, None, None,
            1,
            None,
            [
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetPatrolEvent')",
                "#int(GuardCaptainVar.get('street_pass', 0) or 0) == 0",
                "#town_street.patrol_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetThugsEvent')",
                "#int(TownStreetFightToday or 0) == 0",
                "#town_street.thug_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetHelpEvent')",
                "#town_street.help_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownRandomChronicleEvent')",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetPatrolEvent')",
                "#int(GuardCaptainVar.get('street_pass', 0) or 0) == 0",
                "#town_street.patrol_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetThugsEvent')",
                "#int(TownStreetFightToday or 0) == 0",
                "#town_street.thug_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetHelpEvent')",
                "#town_street.help_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownRandomChronicleEvent')",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetPatrolEvent')",
                "#int(GuardCaptainVar.get('street_pass', 0) or 0) == 0",
                "#town_street.patrol_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetThugsEvent')",
                "#int(TownStreetFightToday or 0) == 0",
                "#town_street.thug_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetHelpEvent')",
                "#town_street.help_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownRandomChronicleEvent')",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetPatrolEvent')",
                "#int(GuardCaptainVar.get('street_pass', 0) or 0) == 0",
                "#town_street.patrol_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetThugsEvent')",
                "#int(TownStreetFightToday or 0) == 0",
                "#town_street.thug_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownStreetHelpEvent')",
                "#town_street.help_allowed(CurLoc)",
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
                "#town_street.location_allowed(CurLoc)",
                "#int(TownStreetEventsToday or 0) < 2",
                "#not town_street.random_seen_this_slot(CurLoc)",
                "#town_street.planned_for(CurLoc, 'TownRandomChronicleEvent')",
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
            "street_clients_liza",
            100,
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
                "#str(TavernMainClientRoomGirl or '') == 'liza'",
                "#int(TavernHole or 0) > 0",
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
                "#church_after_cermon_action_visible()",
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
    LThreadData(0, "georgett", "ChurchServiceBench", None, [
        (
            "story_georgett_church_service_bench",
            7, (8, 9), None,
            1,
            None,
            [
                "#church_service_action_visible()",
                "#bool(Georgett.known) or people_to_int(Georgett.rel, 0) > 0",
                "#npc_schedule_georgett_church_visible()",
                "#people_to_int(Georgett.story_value('foundinchurch', 0), 0) > 0",
                "#Georgett.can_player_cum()",
                "#people_to_int(Georgett.rel, 0) >= 6",
                "#people_to_int(Georgett.corruption, 0) >= 50",
                "#people_to_int(Georgett.sex_stat('sexacts', 0), 0) >= 3",
            ],
            None,
            "Church",
            "georgett_church_service_bench",
            100,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "georgett", "ChurchServiceDoggy", None, [
        (
            "story_georgett_church_service_doggy",
            7, (8, 9), None,
            1,
            None,
            [
                "#church_service_action_visible()",
                "#bool(Georgett.known) or people_to_int(Georgett.rel, 0) > 0",
                "#npc_schedule_georgett_church_visible()",
                "#people_to_int(Georgett.story_value('foundinchurch', 0), 0) > 0",
                "#Georgett.can_player_cum()",
                "#people_to_int(Georgett.rel, 0) >= 6",
                "#people_to_int(Georgett.corruption, 0) >= 50",
                "#people_to_int(Georgett.sex_stat('sexacts', 0), 0) >= 3",
            ],
            None,
            "Church",
            "georgett_church_service_doggy",
            100,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "georgett", "ChurchServiceWithLiza", None, [
        (
            "story_georgett_church_service_with_liza",
            7, (8, 9), None,
            1,
            None,
            [
                "#church_service_action_visible()",
                "#bool(Georgett.known) or people_to_int(Georgett.rel, 0) > 0",
                "#npc_schedule_georgett_church_visible()",
                "#people_to_int(Georgett.story_value('foundinchurch', 0), 0) > 0",
                "#people_to_int(Georgett.story_value('askkids', 0), 0) > 0",
                "#people_to_int(Georgett.story_value('fuckinchurch', 0), 0) > 0",
                "#Georgett.can_player_cum()",
                "#people_to_int(Georgett.rel, 0) >= 6",
                "#people_to_int(Georgett.corruption, 0) >= 50",
                "#people_to_int(Georgett.sex_stat('sexacts', 0), 0) >= 3",
            ],
            None,
            "Church",
            "georgett_church_service_with_liza",
            100,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "georgett", "PortStreetClients", None, [
        (
            "story_georgett_portstreet_clients",
            None, None, None,
            1,
            None,
            [
                "#Georgett.portstreet_client_event_available()",
            ],
            None,
            "PortStreets",
            "street_clients_georgett",
            100,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "georgett", "TavernClientRoom", None, [
        (
            "TavernProstClients",
            None, (13, 15), None,
            1,
            None,
            [
                "#Georgett.can_work_tavern()",
                "#str(TavernMainClientRoomGirl or '') == 'georgett'",
                "#int(TavernHole or 0) > 0",
                "#CheckIfSexEventExist('georgett', 3, 'Prostitution') > 0",
            ],
            None,
            "TavernEmptyRoom",
            "tavern_client_room",
            100,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "georgett", "ChurchAfterSermon", None, [
        (
            "story_georgett_church_after_sermon",
            7, (11, 12), None,
            1,
            None,
            [
                "#church_after_cermon_action_visible()",
                "#Georgett.church_after_sermon_event_available()",
            ],
            None,
            "Church",
            "after_cermon_walk",
            110,
        ),
    ], highlight=False, threaded=False),
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
        ("story_give_birth_sandra", None, None, None, 1, None, ["#int(dayspassed or 0) > 0", "#Sandra.pregnancy_days() >= 240", "#str(Sandra.sex_stat('pregfather', '') or '') != ''"], None, "TavernMain", "enter", 5),
        ("story_give_birth_melissa", None, None, None, 1, None, ["#int(dayspassed or 0) > 0", "#Melissa.pregnancy_days() >= 240", "#str(Melissa.sex_stat('pregfather', '') or '') != ''"], None, "TavernMain", "enter", 6),
        ("story_give_birth_becky", None, None, None, 1, None, ["#int(dayspassed or 0) > 0", "#Becky.pregnancy_days() >= 240", "#str(Becky.stats.get('pregfather', '') or '') != ''"], None, "BeckyHome", "enter", 5),
        ("story_give_birth_inga", None, None, None, 1, None, ["#int(dayspassed or 0) > 0", "#Inga.pregnancy_days() >= 240", "#str(Inga.sex_stat('pregfather', '') or '') != ''"], None, "BeckyHome", "enter", 6),
        ("story_give_birth_georgett", None, None, None, 1, None, ["#int(dayspassed or 0) > 0", "#Georgett.pregnancy_days() >= 240", "#str(Georgett.sex_stat('pregfather', '') or '') != ''"], None, "PortStreets", "enter", 5),
        ("story_give_birth_liza", None, None, None, 1, None, ["#int(dayspassed or 0) > 0", "#Liza.pregnancy_days() >= 240", "#str(Liza.sex_stat('pregfather', '') or '') != ''"], None, "PortStreets", "enter", 6),
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
