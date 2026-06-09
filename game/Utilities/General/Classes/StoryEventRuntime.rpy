# ================================================================================
# FamilyLife-style story event runtime split.
# Engine code lives in conditions.rpy, threads.rpy, and events.rpy.
# Authored thread definitions and event labels stay in StoryEventRuntime.rpy for now.
# ================================================================================

define amandaThreadList = []

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
                "#not (int(WerecatVar.get('sold', 0) or 0) == 0 and int(WerecatVar.get('adopted_count', 0) or 0) >= 1)",
                "#int(WerecatVar.get('rats_problem_active', 0) or 0) == 1",
                "#int(Melissa.var.get('storage_rat_cleared', 0) or 0) == 1",
                "#int(Melissa.var.get('storage_rat_last_help_day', -1) or -1) >= 0",
                "#int(WerecatVar.get('adopted', 0) or 0) == 0",
                "#int(WerecatVar.get('sold', 0) or 0) == 0",
                "#int(WerecatVar.get('hunter_tease_day', -1) or -1) < 0",
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
                "#int(WerecatVar.get('rats_problem_active', 0) or 0) == 1",
                "#int(WerecatVar.get('rat_breakfast_seen', 0) or 0) == 0",
                "#int(WerecatVar.get('hunter_tease_day', -1) or -1) >= 0",
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
                "#int(WerecatVar.get('adopted', 0) or 0) == 1",
                "#int(WerecatVar.get('adoption_breakfast_seen', 0) or 0) == 0",
                "#int(WerecatVar.get('adopted_day', -1) or -1) >= 0",
                "#day_delta_ready(WerecatVar.get('adopted_day', -1), 1)",
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
                "#int(WerecatVar.get('adopted', 0) or 0) == 1",
                "#int(WerecatVar.get('adoption_breakfast_seen', 0) or 0) == 1",
                "#int(WerecatVar.get('adopted_day', -1) or -1) >= 0",
                "#day_delta_ready(WerecatVar.get('adopted_day', -1), 30)",
                "#int(WerecatVar.get('first_month_thanks_day', -1) or -1) < int(WerecatVar.get('adopted_day', -1) or -1) + 30",
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
    #
    # melissa_clarissa_overheard_lead
    #
    LThreadData(0, "melissa", "ClaraOverheard", None, [
        (
            "melissaClaraOverheard_0",
            None, (11, 12), None,
            1,
            None,
            [
                "#str(getLocation('melissa') or '') == 'TavernMain'",
                "#str(getLocation('clara') or '') == 'TavernMain'",
                "#not household_runtime_event_seen_today('melissa_clara_overhear')",
                "#int(ClaraVar.get('tavern_melissa_visit_count', 0) or 0) >= 1",
                "#int(ClaraVar.get('tavern_melissa_overheard_2_seen', 0) or 0) == 0",
            ],
            None,
            "TavernMain",
            "overheard",
            0,
        ),
        (
            "melissaClaraOverheard_1",
            None, (11, 12), None,
            1,
            None,
            [
                "#str(getLocation('melissa') or '') == 'TavernMain'",
                "#str(getLocation('clara') or '') == 'TavernMain'",
                "#not household_runtime_event_seen_today('melissa_clara_overhear')",
                "#int(ClaraVar.get('tavern_melissa_overheard_2_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('tavern_melissa_overheard_3_seen', 0) or 0) == 0",
                "#int(ClaraVar.get('tavern_melissa_visit_count', 0) or 0) >= 2",
                "#int(AmandaVar.get('attic_window_busted', 0) or 0) == 1",
                "#int(Melissa.var.get('bats_episode', 0) or 0) >= 6",
            ],
            None,
            "TavernMain",
            "overheard",
            1,
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
                "#clara_market_daytime_roll_active(dayspassed, week)",
                "#int(ClaraVar.get('booklet_market_seen', 0) or 0) == 0",
                "#not (int(ClaraVar.get('market_follow_failed_day', -1) or -1) == int(dayspassed or 0) and int(ClaraVar.get('market_follow_failed_hour', -1) or -1) == int(hour or 0))",
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
                "#clara_market_evening_roll_active(dayspassed, week)",
                "#int(ClaraVar.get('booklet_market_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('market_evening_intro_seen', 0) or 0) == 0",
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
                "#clara_market_evening_roll_active(dayspassed, week)",
                "#int(ClaraVar.get('market_evening_intro_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('mongol_theft_seen', 0) or 0) == 0",
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
                "#int(ClaraVar.get('mongol_theft_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('escape_confessed', 0) or 0) == 0",
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
                "#int(ClaraVar.get('escape_confessed', 0) or 0) == 1",
                "#int(MongolVar.get('StocksArrestDay', -1) or -1) < 0",
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
                "#int(MongolVar.get('StocksArrestDay', -1) or -1) >= 0",
                "#int(MongolVar.get('StocksSeen', 0) or 0) == 0",
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
                "#int(MongolVar.get('StocksSeen', 0) or 0) == 1",
                "#int(MongolVar.get('StocksFoodDay', -1) or -1) < 0",
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
                "#int(MongolVar.get('StocksFoodDay', -1) or -1) >= 0",
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
                "#int(MongolVar.get('StocksReleased', 0) or 0) == 0",
                "#int(dayspassed or 0) > int(MongolVar.get('StocksFoodDay', -1) or -1)",
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
                "#int(ClaraVar.get('paintings_melissa_asked', 0) or 0) == 0",
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
                "#int(ClaraVar.get('paintings_melissa_asked', 0) or 0) == 1",
                "#int(ClaraVar.get('cellar_seen', 0) or 0) == 0",
                "#int(ClaraVar.get('flirt', 0) or 0) > 0",
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
                "#int(ClaraVar.get('comfort_pending', 0) or 0) == 1",
                "#int(ClaraVar.get('comfort_done', 0) or 0) == 0",
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
                "#int(ClaraVar.get('second_ask_unlocked', 0) or 0) == 1",
                "#int(ClaraVar.get('source_known', 0) or 0) == 0",
            ],
            None,
            "WineStore",
            "clara_talk",
            3,
        ),
        (
            "story_clara_paintings_church_4",
            7, (6, 12), None,
            1,
            None,
            [
                "#int(ClaraVar.get('source_known', 0) or 0) == 1",
                "#int(ClaraVar.get('fiance_church_seen', 0) or 0) == 0",
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
                "#int(ClaraVar.get('fiance_church_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('fiance_barber_seen', 0) or 0) == 0",
                "#(8 <= int(hour or 0) <= 10 or ((int(hour or 0) >= 23 or int(hour or 0) <= 5) and int(ClaraVar.get('fiance_barber_night_roll', 0) or 0) == 1))",
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
                "#int(ClaraVar.get('fiance_barber_seen', 0) or 0) == 1",
                "#int(ClaraVar.get('commission_started', 0) or 0) == 0",
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
                "#int(ClaraVar.get('commission_started', 0) or 0) == 1",
                "#int(ClaraVar.get('commission_followup_done', 0) or 0) == 0",
                "#int(dayspassed or 0) >= int(ClaraVar.get('commission_followup_day', 999999) or 999999)",
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
                "#int(ClaraVar.get('commission_followup_done', 0) or 0) == 1",
                "#int(ClaraVar.get('peek_done', 0) or 0) == 0",
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
                "#int(ClaraVar.get('peek_done', 0) or 0) == 1",
                "#int(ClaraVar.get('confession_done', 0) or 0) == 0",
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
                "#int(ClaraVar.get('confession_done', 0) or 0) == 1",
                "#int(ClaraVar.get('murder_seen', 0) or 0) == 0",
                "#int(dayspassed or 0) >= int(ClaraVar.get('murder_day', 999999) or 999999)",
            ],
            None,
            "CityGuard",
            "enter",
            10,
        ),
    ], highlight=False, threaded=True),
]
define beckyThreadList = []
define eddieThreadList = []
define irmaThreadList = []
define churchThreadList = []
define mongolThreadList = []
define cityGuardThreadList = []
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
        (
            "TavernWorkEventTrigger", None, None, None,
            1,
            None,
            [
                "#tavern_work_planned_for('AmandaLizaTalk', CurLoc, time)",
            ],
            None,
            "TavernMain",
            "tavern_work",
            230,
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
                "#bool(Georgett.known) or bool(knowsMC.get('georgett', False)) or people_to_int(Georgett.rel, 0) > 0",
                "#npc_schedule_georgett_church_visible()",
                "#people_to_int(Georgett.story_value('foundinchurch', 0), 0) > 0",
                "#people_to_int(cametoday, 0) < people_to_int(cancumdaily, 0)",
                "#people_to_int(Friends.get('georgett', Georgett.rel), 0) >= 6",
                "#people_to_int(Georgett.rel, 0) >= 6",
                "#people_to_int(sluttiness.get('georgett', Georgett.corruption), 0) >= 50",
                "#people_to_int(Georgett.corruption, 0) >= 50",
                "#people_to_int(HadSex.get('georgett', 0), 0) >= 3",
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
                "#bool(Georgett.known) or bool(knowsMC.get('georgett', False)) or people_to_int(Georgett.rel, 0) > 0",
                "#npc_schedule_georgett_church_visible()",
                "#people_to_int(Georgett.story_value('foundinchurch', 0), 0) > 0",
                "#people_to_int(cametoday, 0) < people_to_int(cancumdaily, 0)",
                "#people_to_int(Friends.get('georgett', Georgett.rel), 0) >= 6",
                "#people_to_int(Georgett.rel, 0) >= 6",
                "#people_to_int(sluttiness.get('georgett', Georgett.corruption), 0) >= 50",
                "#people_to_int(Georgett.corruption, 0) >= 50",
                "#people_to_int(HadSex.get('georgett', 0), 0) >= 3",
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
                "#bool(Georgett.known) or bool(knowsMC.get('georgett', False)) or people_to_int(Georgett.rel, 0) > 0",
                "#npc_schedule_georgett_church_visible()",
                "#people_to_int(Georgett.story_value('foundinchurch', 0), 0) > 0",
                "#people_to_int(Georgett.story_value('askkids', 0), 0) > 0",
                "#people_to_int(Georgett.story_value('fuckinchurch', 0), 0) > 0",
                "#people_to_int(cametoday, 0) < people_to_int(cancumdaily, 0)",
                "#people_to_int(Friends.get('georgett', Georgett.rel), 0) >= 6",
                "#people_to_int(Georgett.rel, 0) >= 6",
                "#people_to_int(sluttiness.get('georgett', Georgett.corruption), 0) >= 50",
                "#people_to_int(Georgett.corruption, 0) >= 50",
                "#people_to_int(HadSex.get('georgett', 0), 0) >= 3",
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

define threadListsByGirl = {
    "amanda": amandaThreadList,
    "melissa": melissaThreadList,
    "sandra": sandraThreadList,
    "clara": claraThreadList,
    "mongol": mongolThreadList,
    "cityguard": cityGuardThreadList,
    "sherwood": sherwoodThreadList,
    "becky": beckyThreadList,
    "eddie": eddieThreadList,
    "irma": irmaThreadList,
    "church": churchThreadList,
    "liza": lizaThreadList,
    "georgett": georgettThreadList,
    "tavern": tavernThreadList,
    "city": cityThreadList,
}

define threadList = (
    amandaThreadList
    + melissaThreadList
    + sandraThreadList
    + claraThreadList
    + mongolThreadList
    + cityGuardThreadList
    + sherwoodThreadList
    + beckyThreadList
    + eddieThreadList
    + irmaThreadList
    + churchThreadList
    + lizaThreadList
    + georgettThreadList
    + tavernThreadList
    + cityThreadList
)

define threadData = loadThreadData(threadList)
default threads = createThreads()


label melissaClaraOverheard_0:
    $ household_mark_runtime_event_seen("melissa_clara_overhear")
    $ ClaraVar["tavern_melissa_overheard_2_seen"] = 1
    $ MainTxt = "Проходя мимо, вы слышите, как Мелисса, едва сдерживая смех, говорит Клариссе: \"Девчонка утром рано встала, песду о лавку почесала и села у окошка сечь, как бобик Жучку станет ебсть\".\n\nКларисса тут же подхватывает, уже совсем не скрывая довольной ухмылки: \"А бобик жарил Жучку раком, чего стесняться им, собакам!\" После этого обе разом заливаются таким дружным хохотом, будто давно уже спелись на этой пошлой волне."
    $ sluttiness["melissa"] = min(100, int(sluttiness.get("melissa", 0) or 0) + 3)
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + 1)
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/tavern_visit.png"):
        call ShowImage("", "", "images/clara/tavern_visit.png")
    $ current_action_title = "Действия в трактире"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Отойти от чужого разговора", Call("TavernMainRestore"))]
    $ story_thread_advance_current()
    return


label melissaClaraOverheard_1:
    $ household_mark_runtime_event_seen("melissa_clara_overhear")
    $ ClaraVar["tavern_melissa_overheard_3_seen"] = 1
    $ MainTxt = "Вы делаете вид, что заняты у барной стойки, но слух сам цепляет веселый шепот за спиной. Мелисса, уже откровенно дурачась, декламирует: \"Если б я была царица, говорит одна девица, я б пизду покрыла лаком и давала только раком\".\n\n\"Ой-ёй,\" тут же тянет Клара с ехидной ухмылкой, \"царь наш был мужичок скромный, у него был хуй огромный...\" Мелисса шутливо хлопает подружку по плечу и отвечает: \"Да говорю же, вот такой\", после чего раздвигает ладони сантиметров на двадцать.\n\nОбе многозначительно косятся на вас, а потом прыскают от смеха, пока вы изо всех сил делаете вид, будто целиком поглощены стойкой и делами трактира."
    $ sluttiness["melissa"] = min(100, int(sluttiness.get("melissa", 0) or 0) + 4)
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + 2)
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/tavern_visit_size.png"):
        call ShowImage("", "", "images/clara/tavern_visit_size.png")
    $ current_action_title = "Действия в трактире"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Сделать вид, что ничего не услышали", Call("TavernMainRestore"))]
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_0:
    $ SignalBlockTime = 1
    $ UI_mode = "event"
    $ current_action_title = "Рынок"
    $ current_action_content = None
    $ _clara_market_intro_seen = int(ClaraVar.get("market_intro_seen", 0) or 0) == 1
    if _clara_market_intro_seen:
        $ MainTxt = "Днем на рынке снова мелькает фигура в легком плаще. Вы узнаете Клариссу раньше, чем она успевает скрыть лицо. Девушка замечает вас, поспешно натягивает капюшон и идет быстрее, будто совершенно не хочет, чтобы ее здесь окликали.\n\nЕсли уж вы хотите узнать, чем она занимается, сейчас самое время попробовать проследить за ней."
    else:
        $ ClaraVar["market_intro_seen"] = 1
        $ MainTxt = "На дневном рынке среди покупателей вы замечаете фигуру в плаще. Сначала это просто случайный силуэт в толпе, но затем вы узнаете Клариссу, дочку своего винного поставщика.\n\nВы уже собираетесь окликнуть ее, но Кларисса, едва встретившись с вами взглядом, поспешно набрасывает на голову капюшон и сразу идет быстрее между рядами лавок. Похоже, у нее здесь какие-то совсем частные дела, и узнавать себя она сейчас не хочет."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/market_day.png"):
        call ShowImage("", "", "images/clara/market_day.png")
    $ current_action_items = [
        MenuItem("Проследить за Клариссой", Call("story_clara_market_booklet_follow")),
        MenuItem("Не вмешиваться", Call("story_clara_market_booklet_ignore")),
    ]
    call screen main_ui
    jump MarketPlace


label story_clara_market_booklet_confront:
    $ ClaraVar["booklet_market_seen"] = 1
    $ ClaraVar["drawings_secret_known"] = 1
    $ ClaraVar["merchant_contact_unlocked"] = 1
    $ _clara_market_bonus = 1
    if str(player_state().appearance.current_dress or "") == "thiefdress":
        $ _clara_market_bonus += 1
    if int(Friends.get("clara", 0) or 0) >= 7:
        $ _clara_market_bonus += 1
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + _clara_market_bonus)
    $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + max(1, _clara_market_bonus - 1))
    if str(player_state().appearance.current_dress or "") == "thiefdress" and int(Friends.get("clara", 0) or 0) >= 7:
        $ MainTxt = "Вы выходите из-за лотка без лишней суеты и даете Клариссе понять, что уже видели похожие непристойные рисунки у Мелиссы. На секунду она белеет, но, заметив ваш бандитский костюм и поняв, что вы не собираетесь устраивать сцену, быстро берет себя в руки.\n\nКларисса коротко просит не устраивать разговор прямо здесь, а таинственный торговец запоминает вас уже без прежней враждебности. Похоже, с этого дня он готов показывать вам свой особый товар не чаще раза в месяц, а сама Кларисса становится с вами заметно откровеннее."
    else:
        $ MainTxt = "Вы подходите ближе и спокойно даете понять Клариссе, что уже видели похожие непристойные рисунки и догадываетесь, чем она тут занимается. Девушка сразу напрягается, но, услышав, что вы не собираетесь ее выдавать, все же выдыхает.\n\nБез долгих разговоров Кларисса просит не поднимать шум на рынке. Торговец рядом молча запоминает вас взглядом. Похоже, теперь и он будет считать вас своим человеком, а сама Кларисса станет откровеннее лишь если решит, что вам действительно можно доверять."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/market_bookletDeal.png"):
        call ShowImage("", "", "images/clara/market_bookletDeal.png")
    $ current_action_title = "Кларисса и тайный торговец"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Отойти и оставить их", Jump("MarketPlace"))]
    return


label story_clara_market_follow_cost:
    $ LastAdvancedMinutes = 30
    $ calendar_v2.advance_minutes(30)
    $ npc_schedule_sync_all()
    $ werecat_sync_profile()
    $ player_state().change_stat("energy", -5)
    call stat
    return


label story_clara_market_restore_room_result:
    $ CurrentRoom = MarketPlaceRoom
    $ CurLoc = "MarketPlace"
    $ location = CurLoc
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    $ current_girl_key = ""
    $ current_object_id = ""
    $ current_action_content = None
    $ main_ui_overlay = ""
    $ main_ui_inventory_dropdown_open = False
    $ action_menu_specs = []
    call ReturnMainUISceneMode
    return


label story_clara_market_booklet_ignore:
    call story_clara_market_follow_cost
    $ ClaraVar["market_follow_failed_day"] = int(dayspassed or 0)
    $ ClaraVar["market_follow_failed_hour"] = int(hour or 0)
    $ MainTxt = "Вы решаете не вмешиваться и позволяете Клариссе скрыться среди торговых рядов."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Рынок"
    $ current_action_content = None
    call story_clara_market_restore_room_result
    return


label story_clara_market_booklet_follow:
    $ SignalBlockTime = 1
    call story_clara_market_follow_cost
    if int(exploration or 0) < 80:
        $ ClaraVar["market_follow_failed_day"] = int(dayspassed or 0)
        $ ClaraVar["market_follow_failed_hour"] = int(hour or 0)
        $ MainTxt = "Вы стараетесь не отстать, но дневной рынок слишком шумный и тесный. Стоит вам замешкаться на пару шагов, как Кларисса ускользает между рядами и будто растворяется среди чужих спин.\n\nПохоже, без лучшей сноровки в слежке вы просто потеряете ее снова."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Рынок"
        $ current_action_content = None
        call story_clara_market_restore_room_result
        return
    $ ClaraVar["booklet_market_seen"] = 1
    $ MainTxt = "На этот раз вы не теряете Клариссу в толпе. Держась в стороне, вы видите, как она сворачивает к неприметному торговцу, которого почти не видно с центральных рядов. Обмен короткий и явно привычный: Кларисса по одной передает ему тонкие книжечки, похожие на небольшие буклеты, а тот быстро сует их в сумку и так же быстро отсчитывает ей деньги.\n\nТеперь уже ясно, что речь идет не о простой прогулке по рынку. Кларисса что-то сбывает через этого таинственного торговца."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/market_bookletDeal.png"):
        call ShowImage("", "", "images/clara/market_bookletDeal.png")
    if thread is not None:
        $ thread.advance()
    $ current_action_title = "Слежка на рынке"
    $ current_action_content = None
    call story_clara_market_restore_room_result
    $ current_action_title = "Слежка на рынке"
    if int(Melissa.var.get("drawings_found", 0) or 0) == 1 or int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1:
        $ current_action_items.insert(0, MenuItem("Подойти к Клариссе и торговцу", Call("story_clara_market_booklet_confront")))
    return


label story_clara_market_booklet_2_direct_follow:
    $ SignalBlockTime = 1
    $ ClaraVar["market_evening_intro_seen"] = 1
    call story_clara_market_follow_cost
    if int(effective_player_exploration() or 0) < 100:
        $ ClaraVar["market_follow_failed_day"] = int(dayspassed or 0)
        $ ClaraVar["market_follow_failed_hour"] = int(hour or 0)
        $ MainTxt = "Закрытый вечерний рынок куда опаснее для слежки, чем дневная толпа. Стоит вам задеть чью-то корзину и чуть замешкаться, как Кларисса вместе с Монголом растворяются в темном закутке между пустеющими рядами. Без лучшей сноровки здесь их не удержать."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Вечерний рынок"
        $ current_action_content = None
        call story_clara_market_restore_room_result
        return
    $ story_thread_advance_current()
    jump story_clara_market_booklet_3


label story_clara_market_booklet_2:
    $ SignalBlockTime = 1
    $ ClaraVar["market_evening_intro_seen"] = 1
    $ MainTxt = "Вечером рынок закрыт, и площадь выглядит почти пустой. У закрытых лавок задержались лишь несколько человек, поэтому фигура в плаще сразу бросается в глаза. Когда она проходит ближе к фонарю, вы узнаете Клариссу.\n\nСтоит ей заметить ваш взгляд, как девушка глубже натягивает капюшон и быстро уходит в сторону закутка у конного торга. Хм. Очень интересно, что она делает здесь в такое время.\n\nПохоже, на этот раз дело идет уже не о книжечках, а о чем-то более грязном."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/market_night.png"):
        call ShowImage("", "", "images/clara/market_night.png")
    elif renpy.loadable("images/market/LocMarketPlace2.jpg"):
        call ShowImage("", "", "images/market/LocMarketPlace2.jpg")
    $ current_action_title = "Вечерний рынок"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Тихо проследить за Клариссой", Call("story_clara_market_booklet_2_direct_follow")),
        MenuItem("Не рисковать", Call("story_clara_market_booklet_2_ignore")),
    ]
    call screen main_ui
    jump MarketPlace


label story_clara_market_booklet_2_ignore:
    $ current_action_title = "Вечерний рынок"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться к своим делам", Jump("MarketPlace"))]
    call screen main_ui
    jump MarketPlace


label story_clara_market_booklet_3:
    $ SignalBlockTime = 1
    $ MainTxt = "На этот раз вы держитесь достаточно далеко и не выдаете себя ни шагом, ни тенью. Кларисса уводит вас к самому краю рынка, где ее уже ждет Монгол. Разговор идет быстро и вполголоса, но вы успеваете разобрать главное.\n\nКларисса велит ему взять не первую попавшуюся клячу, а хорошую лошадь, чтобы потом продать ее с наваром. Деньги она требует делить честно, потому что именно она нашла покупателя и подсказала, где можно взять товар так, чтобы шум поднялся не сразу. Монгол в ответ ухмыляется, обещает свою долю и, будто нарочно, поддевает ее, что в ее любимом бандитском костюме она выглядела бы среди его людей вовсе как своя.\n\nТеперь уже ясно, что Кларисса не просто прячет от вас книжечки. Она сознательно полезла в настоящую грязь."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/market_night.png"):
        call ShowImage("", "", "images/clara/market_night.png")
    elif renpy.loadable("images/market/mistery_merchant.png"):
        call ShowImage("", "", "images/market/mistery_merchant.png")
    $ ClaraVar["mongol_theft_seen"] = 1
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + 1)
    if renpy.loadable("images/clara/mongolTalk.png"):
        call ShowImage("", "", "images/clara/mongolTalk.png")
    $ current_action_title = "Подслушанный сговор"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Запомнить услышанное и уйти", Jump("MarketPlace"))]
    $ story_thread_advance_current()
    call screen main_ui
    jump MarketPlace


label story_clara_market_booklet_4:
    $ SignalBlockTime = 1
    $ ClaraVar["escape_confessed"] = 1
    $ ClaraVar["drawings_secret_known"] = 1
    $ _clara_escape_bonus = 1
    if str(player_state().appearance.current_dress or "") == "thiefdress":
        $ _clara_escape_bonus += 1
    if int(Friends.get("clara", 0) or 0) >= 7:
        $ _clara_escape_bonus += 1
    $ otkroven["clara"] = min(20, int(otkroven.get("clara", 0) or 0) + _clara_escape_bonus)
    $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + max(1, _clara_escape_bonus - 1))
    $ MainTxt = "Вы дожидаетесь удобного момента и без окриков говорите Клариссе, что видели ее вечерний разговор с Монголом. Девушка сначала белеет, потом зло сжимает губы, но быстро понимает, что вы пришли не сдавать ее отцу.\n\n\"Да, это я его подбила,\" признается она наконец. \"Мне нужны деньги. Отец уже подбирает мне старого хрыча в столице, и весь этот брак будет не для меня, а для его торговли. Я не собираюсь ехать туда смирной куклой.\" Она нервно усмехается и добавляет, что книжечки, рисунки и все разговоры про свободу для нее давно перестали быть просто романтической чушью. \"Хочется хоть раз жить не по чужому счету. А Монгол обещал, что если я соберу достаточно денег, то в его тайном кругу мне найдут место. Хоть кем. Хоть рисовальщицей, хоть этой их девкой для сценок. Знаю, звучит грязно. Но это все равно лучше, чем лечь под старого вонючего дурака по приказу отца.\"\n\nСказав это, Кларисса смотрит на вас уже не как на случайного покупателя, а как на человека, который теперь знает слишком много."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/clara/mongolTalk.png"):
        call ShowImage("", "", "images/clara/mongolTalk.png")
    $ current_action_title = "Откровение Клариссы"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Оставить услышанное между вами", Call("IntClaraTalkRefresh", "clara"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_wine_talk_direct:
    call preEvent("claraBookletMarket")
    if thread is not None and int(thread.num or 0) < 3:
        $ thread.advanceTo(3)
    $ evalTime = None
    $ findAvailableEvents(True)
    jump story_clara_market_booklet_4


label story_clara_market_booklet_5:
    $ SignalBlockTime = 1
    $ MongolVar["StocksArrestDay"] = int(dayspassed or 0)
    $ MainTxt = "Едва вы входите в охотничий клуб, как из угла до вас доносится горячий пересказ свежей городской новости. Охотники с явным удовольствием обсуждают, как стража наконец-то сцапала конокрада, слишком уж долго крутившегося вокруг рынка и конного торга.\n\n\"Сидит теперь у караулки в колодках, вместе с парой таких же голодранцев,\" хмыкает один. \"Пусть народ посмотрит, может поумнеют.\" Другой замечает, что десятник Циммерман теперь ходит важный, как будто сам лично всю шайку выволок за шкирку.\n\nСудя по обрывкам слов, речь идет о Монголе."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/general/hunter_store_catInfo.png"):
        call ShowImage("", "", "images/general/hunter_store_catInfo.png")
    $ current_action_title = "Охотничьи слухи"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Идти проверить колодки у караулки", Jump("CityGuard")), MenuItem("Остаться в охотничьем клубе", Call("HunterClubRestore"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_6:
    $ SignalBlockTime = 1
    $ MongolVar["StocksSeen"] = 1
    $ MainTxt = "На рыночной площади, возле караулки, стоят тяжелые колодки. В них вместе с еще парой помятых головорезов сидит и Монгол. От прежней ярмарочной ухмылки в нем мало что осталось: губа разбита, рубаха грязная, но глаза все еще бегают живо.\n\nЗаметив вас, он дергается и шипит сквозь зубы: \"Стефан, брат, не губи. Я тут с голоду загнусь раньше, чем меня судить начнут. Принеси ночью пожрать, а там, может, и поговорим. Я добро помню. И про Клариссу тоже помню.\""
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/mongolStock.png"):
        call ShowImage("", "", "images/mongolStock.png")
    $ current_action_title = "Монгол в колодках"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Запомнить его просьбу", Call("CityGuardRestore"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_city_guard_direct:
    call preEvent("claraBookletMarket")
    if thread is not None and int(thread.num or 0) < 5:
        $ thread.advanceTo(5)
    $ evalTime = None
    $ findAvailableEvents(True)
    jump story_clara_market_booklet_6


label story_clara_market_booklet_7:
    $ SignalBlockTime = 1
    $ MainTxt = "Ночью у караулки тихо, только где-то внутри переговариваются сонные стражи. Монгол в колодках шевелится и, увидев вас, сразу подается вперед.\n\n\"Ну что, принес чего-нибудь?\" шепчет он. \"Я тут второй день на одной воде. Помоги сейчас, и я потом не забуду.\""
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/mongolStock.png"):
        call ShowImage("", "", "images/mongolStock.png")
    $ current_action_title = "Ночная караулка"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Уйти и вернуться позже", Call("CityGuardRestore"))]
    if int(productnum or 0) > 0:
        $ current_action_items.insert(0, MenuItem("Передать Монголу еду из трактира", Call("story_clara_market_booklet_feed_mongol")))
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label story_clara_market_booklet_feed_mongol:
    $ productnum = max(0, int(productnum or 0) - 1)
    $ MongolVar["StocksFoodDay"] = int(dayspassed or 0)
    $ MainTxt = "Вы незаметно протягиваете Монголу завернутую в тряпицу еду из трактирной кухни. Тот жадно хватается за нее обеими руками, давится первыми кусками и тут же начинает шептать благодарности.\n\n\"Вот это по-людски, Стефан. Еще бы отмычки добыть, да стражу чем-нибудь отвлечь... Тогда я не просто вылезу, а еще и твой долг запомню. Если потом занесет к людям Робина, скажу им, кто ты такой.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Ночная караулка"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Оставить Монгола жевать в темноте", Call("CityGuardRestore"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_feed_mongol_direct:
    call preEvent("claraBookletMarket")
    if thread is not None and int(thread.num or 0) < 6:
        $ thread.advanceTo(6)
    $ evalTime = None
    $ findAvailableEvents(True)
    jump story_clara_market_booklet_feed_mongol


label story_clara_market_booklet_8:
    $ SignalBlockTime = 1
    $ MainTxt = "Вы находите Драупнира за верстаком и, не мудрствуя лукаво, объясняете, что вам нужны очень тонкие отмычки. Гном сперва косится на вас с подозрением, потом только фыркает.\n\n\"Ничего не знаю и знать не хочу, для какой двери тебе такая железяка,\" ворчит он. \"Но если работа тонкая и молчаливая, то это ко мне. За сорок мараведи сделаю хороший набор, который и в сапог спрятать не стыдно.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Заказ у Драупнира"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Не заказывать пока", Call("StolyarWorkshopBuildActions"))]
    if int(money or 0) >= 40:
        $ current_action_items.insert(0, MenuItem("Заплатить 40 мараведи за тонкие отмычки", Call("story_clara_market_booklet_lockpicks_order")))
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label story_clara_market_booklet_lockpicks_order:
    $ money = int(money or 0) - 40
    $ DraupnirVar["MongolLockpickOrderDay"] = int(dayspassed or 0)
    $ MainTxt = "Драупнир быстро прячет деньги, вытаскивает из ящика тонкий кожаный сверток и сует его вам почти не глядя.\n\n\"Вот. Только если с этим полезешь куда не надо, не вздумай потом ссылаться на меня,\" бурчит гном. Судя по тяжести свертка, набор отмычек у вас теперь есть."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Заказ у Драупнира"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Спрятать сверток и уйти", Call("StolyarWorkshopBuildActions"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_lockpicks_order_direct:
    call preEvent("claraBookletMarket")
    if thread is not None and int(thread.num or 0) < 7:
        $ thread.advanceTo(7)
    $ evalTime = None
    $ findAvailableEvents(True)
    jump story_clara_market_booklet_lockpicks_order


label story_clara_market_booklet_9:
    $ SignalBlockTime = 1
    $ MainTxt = "Следующей ночью вы возвращаетесь к караулке уже подготовленным. Монгол сразу понимает это по вашему лицу и только сильнее вжимается в колодки, чтобы не привлекать лишних взглядов.\n\nТеперь все упирается в одно: если вы хотите вытащить его отсюда, надо сперва умаслить стражу и отвлечь ее чем-то приятнее ночного дежурства."
    $ CurLocDesc = MainTxt
    if renpy.loadable("images/mongolStock.png"):
        call ShowImage("", "", "images/mongolStock.png")
    $ current_action_title = "Побег Монгола"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Передумать и уйти", Call("CityGuardRestore"))]
    if int(productnum or 0) > 0 and int(winenum or 0) > 0:
        $ current_action_items.insert(0, MenuItem("Послать стражникам вино и угощение, а затем освободить Монгола", Call("story_clara_market_booklet_release_mongol")))
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label story_clara_market_booklet_release_mongol:
    $ productnum = max(0, int(productnum or 0) - 1)
    $ winenum = max(0, int(winenum or 0) - 1)
    $ tavernfame = int(tavernfame or 0) + 2
    $ Friends["zimmer"] = min(20, int(Friends.get("zimmer", 0) or 0) + 1)
    $ MongolVar["GuardGiftSent"] = 1
    $ MongolVar["GuardCaptainKnown"] = 1
    $ MongolVar["StocksReleased"] = 1
    $ RobinVar["MongolSafePass"] = 1
    $ MainTxt = "Вы заранее посылаете к караулке кувшин вина и хороший ужин из трактира с вежливой припиской: мол, \"Дикий Жеребец\" благодарит городскую стражу за поимку конокрадов. Стража мгновенно добреет к такой заботе. Сам десятник Циммерман замечает, что вот это уже разговор с уважаемым трактирщиком, который умеет ценить порядок в городе.\n\nКогда угощение делает свое дело и дежурные окончательно расслабляются, вы выбираете момент, приседаете к колодкам и пускаете в ход заказанные у Драупнира отмычки. Замок поддается не сразу, но все же тихо щелкает. Монгол выскальзывает из дерева, как уж, шепотом сыплет вам благодарностями и обещает, что люди Робина в Шервуде узнают, кому он обязан свободой.\n\nЕще до рассвета его и след простыл."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Побег Монгола"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Раствориться в ночи", Call("CityGuardRestore"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    $ story_thread_advance_current()
    return


label story_clara_market_booklet_release_mongol_direct:
    call preEvent("claraBookletMarket")
    if thread is not None and int(thread.num or 0) < 8:
        $ thread.advanceTo(8)
    $ evalTime = None
    $ findAvailableEvents(True)
    jump story_clara_market_booklet_release_mongol
