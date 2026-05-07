# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitSandra:
    python:
        knowsMC["sandra"] = True
        # Initialize Sandra's attributes
        GirlName = 'sandra'

        RealName[GirlName] = 'Сандра'
        RealName2[GirlName] = 'Сандры'
        RealName3[GirlName] = 'Сандре'
        age_girls[GirlName] = 34
        DateOfBirth[GirlName] = calendar_make_birth_record(age_girls[GirlName])
        kids[GirlName] = 3
        beauty[GirlName] = 65
        sluttiness[GirlName] = 20
        sexacts[GirlName] = 4352
        cuminside[GirlName] = 2593
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ''
        ConceptionChance[GirlName] = 5
        CurrentLoc[GirlName] = 'TavernMain'
        PussyWetStart[GirlName] = 20
        virginity[GirlName] = False

        # Description and default dress
        girltextdesc[GirlName] = 'Сандра - женщина в самом соку. У нее темные волосы, зеленые глаза и грудь размера DD.'
        dressdefault[GirlName] = 'workdresszhilet'

        # Default clothing
        bradef[GirlName] = 'simplebra'
        pantiesdef[GirlName] = 'simplepanties'
        legsdef[GirlName] = ''
        shoesdef[GirlName] = 'simpleshoes'

        # Skills
        cooking[GirlName] = 90
        cleaning[GirlName] = 70
        waitress[GirlName] = 20

        # Job-related data
        otkroven[GirlName] = 0
        jobkitchen[GirlName] = 1
        jobcleaning[GirlName] = 0
        jobwaitress[GirlName] = 0
        Friends[GirlName] = 5
        jobHallAvail[GirlName] = 1
        jobWhoreAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0

        # Custom variables
        SandraVar['knowmolodost'] = 0
        SandraVar['WeeklyChoreCheckScore'] = 0
        SandraVar['WeeklyChoreCheckCounter'] = 0
        SandraVar['Week5WakePending'] = 0
        SandraVar['WeeklyChoreCheckEval'] = ''
        SandraVar['RoomUnlocked'] = 0
        SandraVar['MCVisitFirstReady'] = 0
        SandraVar['MCVisitFirstPending'] = 0
        SandraVar['MCVisitFirstDone'] = 0
        SandraVar['NightThanksReady'] = 0
        SandraVar['NightThanksLastDay'] = -1
        GiftPreferences[GirlName] = ["soap_001", "wild_rose_001", "lavender_001", "berries_001", "mushroom_001", "honey_comb_001", "energy_tea_001", "drink_ale_001"]
        npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[3], awake=True, talkable=True, condition=npc_schedule_rule("sandra_night_thanks_ready"), priority=380, label="night_thanks"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernMain", mode="morning"), priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernKitchen", mode="morning"), priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernStorage", mode="morning"), priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="Backyard", mode="morning"), priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernSandraRoom", mode="morning"), priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_kitchen"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="FridayDance", mode="friday_evening"), priority=250, label="friday_dance"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernSandraRoom", mode="friday_evening"), priority=240, label="friday_room"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernSandraRoom", mode="sunday"), priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="Backyard", mode="sunday"), priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernMain", mode="sunday"), priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="sandra", location="TavernKitchen", mode="sunday"), priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernSandraRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[4], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
        npc_schedule_sync_currentloc(GirlName)

    return
