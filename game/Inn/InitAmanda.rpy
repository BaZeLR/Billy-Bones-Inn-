init 4 python:
    import random

    def amanda_has_given_night_bowl():
        return int(AmandaVar.get("gave_night_bowl", 0) or 0) == 1

    def amanda_can_be_asked_for_night_bowl():
        return (
            player_has_soap_recipe_book()
            and not amanda_has_given_night_bowl()
            and _player_item_count_by_id("night_bowl_001") <= 0
            and int(AmandaVar.get("night_bowl_request_day", -1) or -1) != int(dayspassed or 0)
        )

    def amanda_can_be_asked_for_night_bowl_favor():
        return (
            amanda_can_be_asked_for_night_bowl()
            and int(Friends.get("amanda", 0) or 0) >= 7
            and int(Drunk.get("amanda", 0) or 0) > 0
        )

    def amanda_night_bowl_success_chance(from_dance=False):
        friendship_value = int(Friends.get("amanda", 0) or 0)
        chance_value = 20 + max(0, friendship_value - 4) * 8
        if from_dance and int(Drunk.get("amanda", 0) or 0) > 0:
            chance_value += 20
        if friendship_value >= 10:
            chance_value = 100
        return max(5, min(100, int(chance_value or 0)))

    def amanda_night_bowl_request_result(from_dance=False):
        if not amanda_can_be_asked_for_night_bowl():
            return {"ok": False, "granted": False, "reason": "unavailable"}

        AmandaVar["night_bowl_request_day"] = int(dayspassed or 0)
        friendship_value = int(Friends.get("amanda", 0) or 0)
        chance_value = amanda_night_bowl_success_chance(from_dance)
        granted = friendship_value >= 10 or random.randint(1, 100) <= chance_value
        if granted:
            _player_add_item_by_id("night_bowl_001", 1)
            AmandaVar["gave_night_bowl"] = 1
            AmandaVar["night_bowl_window_seen_day"] = -1
            return {"ok": True, "granted": True, "chance": chance_value}
        return {"ok": True, "granted": False, "chance": chance_value}

    def amanda_night_bowl_window_event_ready():
        return (
            amanda_has_given_night_bowl()
            and _player_item_count_by_id("night_bowl_001") > 0
            and (
                int(AmandaVar.get("got_fancy_night_bowl", 0) or 0) == 0
                or int(AmandaVar.get("prefers_backyard_relief", -1) or -1) == 1
            )
            and int(time or 0) >= 4
            and int(AmandaVar.get("night_bowl_window_seen_day", -1) or -1) != int(dayspassed or 0)
        )

    def amanda_can_receive_fancy_night_bowl():
        return (
            amanda_has_given_night_bowl()
            and int(AmandaVar.get("got_fancy_night_bowl", 0) or 0) == 0
            and _player_item_count_by_id("fancy_night_bowl_001") > 0
        )

    def amanda_prefers_backyard_relief():
        return int(AmandaVar.get("prefers_backyard_relief", -1) or -1) == 1

    def amanda_pick_backyard_relief_preference():
        friendship_value = int(Friends.get("amanda", 0) or 0)
        sluttiness_value = int(sluttiness.get("amanda", 0) or 0)
        chance_value = 20 + friendship_value * 4 + int(sluttiness_value / 5)
        if int(AmandaVar.get("gave_night_bowl", 0) or 0) == 1:
            chance_value += 10
        chance_value = max(5, min(90, chance_value))
        AmandaVar["prefers_backyard_relief"] = 1 if random.randint(1, 100) <= chance_value else 0
        return int(AmandaVar.get("prefers_backyard_relief", 0) or 0)

label InitAmanda:
    python:
        knowsMC["amanda"] = True
        # Initialize Amanda's attributes
        GirlName = 'amanda'

        RealName[GirlName] = 'Аманда'
        RealName2[GirlName] = 'Аманды'
        RealName3[GirlName] = 'Аманде'
        age_girls[GirlName] = 18
        DateOfBirth[GirlName] = calendar_make_birth_record(age_girls[GirlName])
        kids[GirlName] = 0
        beauty[GirlName] = 52
        sluttiness[GirlName] = 0
        sexacts[GirlName] = 0
        cuminside[GirlName] = 0
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ''
        ConceptionChance[GirlName] = 10
        CurrentLoc[GirlName] = 'TavernMain'
        PussyWetStart[GirlName] = 0
        virginity[GirlName] = True

        # Description and default dress
        girltextdesc[GirlName] = 'Аманда - молодая девушка. У нее очень светлая кожа, белокурые волосы и голубые глаза. Ее груди небольшие, размера А.'
        dressdefault[GirlName] = 'modestworkdress'

        # Default clothing
        bradef[GirlName] = 'simplebra'
        pantiesdef[GirlName] = 'simplepanties'
        legsdef[GirlName] = ''
        shoesdef[GirlName] = 'simpleshoes'

        # Skills
        cooking[GirlName] = 20
        cleaning[GirlName] = 30
        waitress[GirlName] = 15

        # Job-related data
        otkroven[GirlName] = 3
        jobkitchen[GirlName] = 0
        jobcleaning[GirlName] = 1
        jobwaitress[GirlName] = 1
        jobHallAvail[GirlName] = 1
        jobWhoreAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0

        # Relationships with Player
        Friends[GirlName] = 5

        # Custom variables (TXT parity)
        AmandaVar['lizafriends'] = 0
        AmandaVar['prohibitliza'] = 0
        AmandaVar['alberfriends'] = 0
        AmandaVar['albernowdances'] = 0
        AmandaVar['alberdanceadvance'] = 0
        AmandaVar['leftdances'] = 0
        AmandaVar['alberprohibit'] = 0
        AmandaVar['LegareGo'] = 0
        AmandaVar['EscapeUnnoticed'] = 0
        AmandaVar['glorytried'] = 0
        AmandaVar['gloryyouknow'] = 0
        AmandaVar['gloryscold'] = 0
        AmandaVar['glorywalkout'] = 0
        AmandaVar['glorysuck'] = 0
        AmandaVar['glorysdiscover'] = 0
        AmandaVar['glorydeflower'] = 0
        AmandaVar['suckyou'] = 0
        AmandaVar['fuckyou'] = 0
        AmandaVar['knowsexactive'] = 0
        AmandaVar['knownotvirgin'] = 0
        AmandaVar['knowlegaresex'] = 0
        AmandaVar['sawlegaresex'] = 0
        AmandaVar['sucklegare'] = 0
        AmandaVar['fucklegare'] = 0
        AmandaVar['deflowerlegare'] = 0
        AmandaVar['knowdeflowerlegare'] = 0
        AmandaVar['beddeflower'] = 0
        AmandaVar['kickyoufromroom'] = 0
        AmandaVar['kickyoufromroomcount'] = 0
        AmandaVar['kickedwithmomhelp'] = 0
        AmandaVar['knowyousawlegaresex'] = 0
        AmandaVar['knowyouseesex'] = 0
        AmandaVar['warnnotwork'] = 0
        AmandaVar['sawwithguys'] = 0
        AmandaVar['prohibitwithguys'] = 0
        AmandaVar['askzalettoday'] = 0
        AmandaVar['MomDressComplaint'] = 0
        AmandaVar['gave_night_bowl'] = 0
        AmandaVar['night_bowl_request_day'] = -1
        AmandaVar['night_bowl_window_seen_day'] = -1
        AmandaVar['got_fancy_night_bowl'] = 0
        AmandaVar['prefers_backyard_relief'] = -1
        AmandaVar['attic_window_busted'] = 0
        AmandaVar['attic_window_breakfast_bj_day'] = -1
        GiftPreferences[GirlName] = ["wild_rose_001", "soap_001", "berries_001", "energy_tea_001", "drink_ale_001"]
        npc_schedule_set(
            GirlName,
            [
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernMain", mode="morning"), priority=300, label="morning_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernKitchen", mode="morning"), priority=300, label="morning_kitchen"),
                NPCScheduleEntry(location="TavernStorage", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernStorage", mode="morning"), priority=300, label="morning_storage"),
                NPCScheduleEntry(location="Backyard", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="Backyard", mode="morning"), priority=300, label="morning_backyard"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernAmandaRoom", mode="morning"), priority=300, label="morning_room"),
                NPCScheduleEntry(location="TavernMain", weekdays=[1, 2, 3, 4, 6], time_slots=[1, 2, 3], awake=True, talkable=True, priority=200, label="working_hall"),
                NPCScheduleEntry(location="FridayDance", weekdays=[5], time_slots=[3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="FridayDance", mode="friday_evening"), priority=250, label="friday_dance"),
                NPCScheduleEntry(location="Church", weekdays=[7], time_slots=[0, 1], awake=True, talkable=False, priority=260, label="sunday_church"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernAmandaRoom", mode="sunday"), priority=240, label="sunday_room"),
                NPCScheduleEntry(location="Backyard", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="Backyard", mode="sunday"), priority=240, label="sunday_backyard"),
                NPCScheduleEntry(location="TavernMain", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernMain", mode="sunday"), priority=240, label="sunday_hall"),
                NPCScheduleEntry(location="TavernKitchen", weekdays=[7], time_slots=[2, 3], awake=True, talkable=True, condition=npc_schedule_rule("tavern_team_match", person="amanda", location="TavernKitchen", mode="sunday"), priority=240, label="sunday_kitchen"),
                NPCScheduleEntry(location="TavernAmandaRoom", weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[4], awake=False, talkable=False, priority=10, label="sleep"),
            ],
        )
        npc_schedule_sync_currentloc(GirlName)

    return
