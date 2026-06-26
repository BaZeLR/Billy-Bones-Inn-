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
        DateOfBirth[GirlName] = {"day": 1, "period": 1, "cycle": 1078}
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
        peopleData[GirlName] = IngaStaticData
        Inga.var = IngaVar
        Inga.location = "BeckyHome"
        Inga.update()
        peopleInfo[GirlName] = Inga
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
                time_slots=[7],
                awake=False,
                talkable=False,
                priority=10,
                label="inga_home_sleep",
            ),
        ])
        npc_schedule_sync_currentloc(GirlName)
    return

init python:
    if 'IngaVar' not in dir() or not isinstance(IngaVar, dict):
        IngaVar = {"SawLucassex": 0, "Knowher": 0}

    def inga_grocery_store_active(weekday_value=None, time_slot=None):
        week_now = int(week if weekday_value is None else weekday_value or 0)
        time_now = int(time if time_slot is None else time_slot or 0)
        if week_now == 7 or time_now != 0:
            return False
        return str(npc_schedule_location("eddie", week_now, time_now) or "") != "GroceryStore"

    if 'SECONDARY_NPC_KEYS' not in dir():
        SECONDARY_NPC_KEYS = []
    if "inga" not in SECONDARY_NPC_KEYS:
        SECONDARY_NPC_KEYS.append("inga")

    class IngaData(PeopleData):
        code_name = "inga"

        def __init__(self):
            super().__init__(
                self.code_name,
                cname="Ингенборг",
                fullname="Ингенборг Блэнкеншип",
                genitive="Ингенборг",
                dative="Ингенборг",
                default_location="BeckyHome",
                description="Старшей дочке вдовы Блэнкеншип в привлекательности не откажешь. Рыжая, высокая, зеленоглазая, с большой налитой грудью, Ингенборг выглядит как молодая и еще более привлекательная копия своей матушки.",
                birth_date={"day": 1, "period": 1, "cycle": 1078},
                portrait="images/inga/StreetSex/minet1.jpg",
            )

    class IngaInfo(BaseNPC):
        """Inga Blankenship: secondary NPC with Becky-home story state."""
        unknown_name = "Незнакомка"

        def __init__(self, name="inga", **kwargs):
            super().__init__(name, **kwargs)
            self.var = kwargs.get("var", IngaVar)
            for k, v in {
                "SawLucassex": 0,
                "Knowher": 0,
            }.items():
                self.var.setdefault(k, v)
            self.location = "BeckyHome"
            self.promote_from_var(self.var)

define IngaStaticData = IngaData()
default Inga = IngaInfo()


label register_inga_secondary:
    $ knowsMC.setdefault("inga", False)
    python:
        if "peopleData" in dir() and isinstance(peopleData, dict):
            peopleData["inga"] = IngaStaticData
        if "peopleInfo" in dir() and isinstance(peopleInfo, dict):
            Inga.var = IngaVar
            Inga.location = "BeckyHome"
            Inga.update()
            peopleInfo["inga"] = Inga
        if 'secondary_npcs' not in dir() or not isinstance(secondary_npcs, list):
            secondary_npcs = []
        if peopleInfo.get("inga") and peopleInfo["inga"] not in secondary_npcs:
            secondary_npcs.append(peopleInfo["inga"])
        if 'girls' in dir() and isinstance(girls, list):
            girls[:] = [row for row in girls if str(getattr(row, "name", "") or "") != "inga"]
    return
