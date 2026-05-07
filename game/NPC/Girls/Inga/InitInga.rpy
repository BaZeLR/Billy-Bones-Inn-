# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitInga:
    python:
        # Initialize Inga's attributes
        GirlName = 'inga'
        RealName[GirlName] = 'Ингенборг'
        RealName2[GirlName] = 'Ингенборг'
        RealName3[GirlName] = 'Ингенборг'
        age_girls[GirlName] = 22
        DateOfBirth[GirlName] = calendar_make_birth_record(age_girls[GirlName])
        kids[GirlName] = 0
        beauty[GirlName] = 55
        sluttiness[GirlName] = 30
        sexacts[GirlName] = 134
        cuminside[GirlName] = 42
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ''
        ConceptionChance[GirlName] = 10
        PussyWetStart[GirlName] = 25
        virginity[GirlName] = False

        girltextdesc[GirlName] = 'Старшей дочке вдовы Блэнкеншип в привлекательности не откажешь. Рыжая, высокая, зеленоглазая, с большой налитой грудью, Ингенборг выглядит как молодая и еще более привлекательная копия своей матушки.'
        dressdefault[GirlName] = 'openworkdress'

        bradef[GirlName] = 'simplebra'
        pantiesdef[GirlName] = 'simplepanties'
        legsdef[GirlName] = 'redstockings'
        shoesdef[GirlName] = 'simpleshoes'

        cooking[GirlName] = 40
        cleaning[GirlName] = 20
        waitress[GirlName] = 40

        otkroven[GirlName] = 0
        jobkitchen[GirlName] = 0
        jobcleaning[GirlName] = 0
        jobwaitress[GirlName] = 0
        Friends[GirlName] = 0
        jobHallAvail[GirlName] = 0
        jobWhoreAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0

        IngaVar['SawLucassex'] = 0
        IngaVar['Knowher'] = 0
        GiftPreferences[GirlName] = ["wild_rose_001", "soap_001", "lavender_001"]
        CurrentLoc[GirlName] = "BeckyHome"
        npc_schedule_set(GirlName, [
            NPCScheduleEntry(
                location="GroceryStore",
                weekdays=[1, 2, 3, 4, 5, 6],
                time_slots=[0],
                awake=True,
                talkable=True,
                condition=inga_grocery_store_active,
                priority=230,
                label="inga_grocery_cover",
            ),
            NPCScheduleEntry(
                location="Church",
                weekdays=[7],
                time_slots=[0, 1],
                awake=True,
                talkable=False,
                priority=220,
                label="inga_sunday_church",
            ),
            NPCScheduleEntry(
                location="BeckyHome",
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                time_slots=[0, 1, 2, 3],
                awake=True,
                talkable=True,
                priority=20,
                label="inga_home_awake",
            ),
            NPCScheduleEntry(
                location="BeckyHome",
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                time_slots=[4],
                awake=False,
                talkable=False,
                priority=10,
                label="inga_home_sleep",
            ),
        ])
        npc_schedule_sync_currentloc(GirlName)
    return

init python:
    def inga_grocery_store_active(weekday_value=None, time_slot=None):
        week_now = int(week if weekday_value is None else weekday_value or 0)
        time_now = int(time if time_slot is None else time_slot or 0)
        if week_now == 7 or time_now != 0:
            return False
        return str(npc_schedule_location("eddie", week_now, time_now) or "") != "GroceryStore"
