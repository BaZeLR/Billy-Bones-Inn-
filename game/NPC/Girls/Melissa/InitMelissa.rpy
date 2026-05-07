# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -1 python:
    def melissa_install_schedule(girl_name="melissa"):
        schedule_name = str(girl_name or "melissa").strip()
        npc_daily_schedule_set(
            schedule_name,
            default_slots=[
                dict(npc_daily_schedule_slot(0, "Church", True, False, "sunday_church"), weekdays=[7]),
                dict(npc_daily_schedule_slot(1, "Church", True, False, "sunday_church"), weekdays=[7]),
                npc_daily_schedule_slot(4, "TavernMelissaRoom", False, False, "sleep"),
            ],
            random_slots=[
                npc_daily_schedule_random_slot(
                    0,
                    weekdays=[1, 2, 3, 4, 5, 6],
                    label="morning",
                    priority=500,
                    choices=[
                        npc_daily_schedule_choice("TavernKitchen", 4, True, True, "breakfast_and_kitchen"),
                        npc_daily_schedule_choice("TavernStorage", 4, True, True, "basement_cleaning"),
                        npc_daily_schedule_choice("TavernMain", 3, True, True, "hall_cleaning"),
                        npc_daily_schedule_choice("Backyard", 2, True, True, "yard_laundry"),
                        npc_daily_schedule_choice("TavernMelissaRoom", 1, True, True, "late_start_room"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    1,
                    weekdays=[1, 2, 3, 4, 5, 6],
                    label="noon_work",
                    priority=420,
                    choices=[
                        npc_daily_schedule_choice("TavernMain", 6, True, True, "working_hall"),
                        npc_daily_schedule_choice("TavernKitchen", 1, True, True, "kitchen_help"),
                        npc_daily_schedule_choice("TavernStorage", 1, True, True, "storage_sorting"),
                        npc_daily_schedule_choice("Backyard", 1, True, True, "yard_chore"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    2,
                    weekdays=[1, 2, 3, 4, 5, 6],
                    label="day_work",
                    priority=420,
                    choices=[
                        npc_daily_schedule_choice("TavernMain", 7, True, True, "working_hall"),
                        npc_daily_schedule_choice("TavernKitchen", 1, True, True, "kitchen_help"),
                        npc_daily_schedule_choice("Backyard", 1, True, True, "yard_chore"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    3,
                    weekdays=[1, 2, 3, 4, 6],
                    label="evening",
                    priority=360,
                    choices=[
                        npc_daily_schedule_choice("TavernMain", 3, True, True, "evening_hall"),
                        npc_daily_schedule_choice("TavernMelissaRoom", 2, True, True, "evening_room"),
                        npc_daily_schedule_choice("Backyard", 1, True, True, "evening_yard"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    3,
                    weekdays=[5],
                    label="friday_evening",
                    priority=360,
                    choices=[
                        npc_daily_schedule_choice("FridayDance", 4, True, True, "friday_dance"),
                        npc_daily_schedule_choice("TavernMelissaRoom", 2, True, True, "friday_room"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    2,
                    weekdays=[7],
                    label="sunday_day",
                    priority=360,
                    choices=[
                        npc_daily_schedule_choice("TavernMelissaRoom", 3, True, True, "sunday_room"),
                        npc_daily_schedule_choice("Backyard", 2, True, True, "sunday_backyard"),
                        npc_daily_schedule_choice("TavernMain", 2, True, True, "sunday_hall"),
                        npc_daily_schedule_choice("TavernKitchen", 1, True, True, "sunday_kitchen"),
                    ],
                ),
                npc_daily_schedule_random_slot(
                    3,
                    weekdays=[7],
                    label="sunday_evening",
                    priority=360,
                    choices=[
                        npc_daily_schedule_choice("TavernMelissaRoom", 3, True, True, "sunday_room"),
                        npc_daily_schedule_choice("Backyard", 1, True, True, "sunday_backyard"),
                        npc_daily_schedule_choice("TavernMain", 2, True, True, "sunday_hall"),
                        npc_daily_schedule_choice("TavernKitchen", 1, True, True, "sunday_kitchen"),
                    ],
                ),
            ],
        )
        npc_schedule_set(
            schedule_name,
            [
                NPCScheduleEntry(location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[3, 4], awake=True, talkable=True, condition=npc_schedule_rule("clara_paintings_confession"), priority=470, label="clara_paintings_confession"),
            ],
        )
        npc_daily_schedule_build_all(True)
        npc_schedule_sync_currentloc(schedule_name)

    def melissa_after_load_schedule():
        try:
            if "melissa" in list(RealName.keys()):
                melissa_install_schedule("melissa")
        except Exception:
            pass

    config.after_load_callbacks.append(melissa_after_load_schedule)

label InitMelissa:
    python:
        knowsMC["melissa"] = True
        # Initialize Melissa's attributes
        GirlName = 'melissa'

        RealName[GirlName] = 'Мелисса'
        RealName2[GirlName] = 'Мелиссы'
        RealName3[GirlName] = 'Мелиссе'
        age_girls[GirlName] = 18
        DateOfBirth[GirlName] = calendar_make_birth_record(age_girls[GirlName])
        kids[GirlName] = 0
        beauty[GirlName] = 55
        sluttiness[GirlName] = 3
        sexacts[GirlName] = 0
        cuminside[GirlName] = 0
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ''
        ConceptionChance[GirlName] = 15
        CurrentLoc[GirlName] = 'TavernMain'
        PussyWetStart[GirlName] = 10
        virginity[GirlName] = True

        # Description and default dress
        girltextdesc[GirlName] = 'Мелисса - молодая девушка. В ее сложении немного проступают восточные черты. Она немного отличается от остальных работниц трактира. У нее оливкового цвета кожа, черные глаза, волосы цвета вороньего крыла и полные, похожие на мячи груди размера С.'
        dressdefault[GirlName] = 'workdress'

        # Default clothing
        bradef[GirlName] = 'simplebra'
        pantiesdef[GirlName] = 'simplepanties'
        legsdef[GirlName] = ''
        shoesdef[GirlName] = 'simpleshoes'

        # Skills
        cooking[GirlName] = 30
        cleaning[GirlName] = 40
        waitress[GirlName] = 30

        # Job-related data
        otkroven[GirlName] = 0
        jobkitchen[GirlName] = 0
        jobcleaning[GirlName] = 1
        jobwaitress[GirlName] = 1
        Friends[GirlName] = 5
        jobHallAvail[GirlName] = 1
        jobWhoreAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0

        # Custom variables
        MelissaVar['MomDressComplaint'] = 0
        MelissaVar['AskedAboutClaraDay'] = -1
        MelissaVar['StartDay'] = -1
        MelissaVar['StartCount'] = 0
        MelissaVar['StartTotal'] = 0
        MelissaVar['private_context_day'] = -1
        MelissaVar['private_context_origin'] = ''
        MelissaVar['private_context_place'] = ''
        MelissaVar['private_place_heat'] = 0
        MelissaVar['RoomProblemAskDay'] = -1
        MelissaVar['StorageThanksDay'] = -1
        MelissaVar['AtticFindingsDay'] = -1
        MelissaVar['bats_episode'] = 0
        MelissaVar['temp_room'] = ''
        MelissaVar['storage_rat_last_help_day'] = -1
        MelissaVar['room_pests_last_help_day'] = -1
        MelissaVar['AskedMCToSolveRoomProblem'] = 0
        MelissaVar['bat_attic_check_day'] = -1
        MelissaVar['drawings_ready_day'] = -1
        MelissaVar['drawings_found'] = 0
        MelissaVar['drawings_returned'] = 0
        MelissaVar['bat_recipe_clue_seen'] = 0
        MelissaVar['bat_recipe_unlocked'] = 0
        MelissaVar['bats_completed'] = 0
        MelissaVar['bats_completion_day'] = -1
        MelissaVar['room_returned'] = 0
        MelissaVar['sex_engine_unlocked'] = 0
        MelissaVar['roof_repair_order_day'] = -1
        MelissaVar['roof_repair_complete_day'] = -1
        MelissaVar['breakfast_tease_day'] = -1
        GiftPreferences[GirlName] = ["soap_001", "lavender_001", "wild_rose_001", "energy_tea_001", "drink_ale_001", "libido_tincture_001"]
        bodymodel_sync_character(GirlName, RealName[GirlName], "female")
        melissa_install_schedule(GirlName)

    return
