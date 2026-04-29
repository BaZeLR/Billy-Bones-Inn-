# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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
        npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="TavernMain", mode="morning"), priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="TavernKitchen", mode="morning"), priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="TavernStorage", mode="morning"), priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="Backyard", mode="morning"), priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="TavernMelissaRoom", mode="morning"), priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2], awake=True, talkable=True, priority=200, label="working_hall"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="FridayDance", mode="friday_evening"), priority=250, label="friday_dance"),
                NPCScheduleEntry(location="TavernMelissaRoom", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="TavernMelissaRoom", mode="friday_evening"), priority=240, label="friday_room"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernMelissaRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="TavernMelissaRoom", mode="sunday"), priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="Backyard", mode="sunday"), priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="TavernMain", mode="sunday"), priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="melissa", location="TavernKitchen", mode="sunday"), priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernMelissaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[4], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
        npc_schedule_sync_currentloc(GirlName)

    return
