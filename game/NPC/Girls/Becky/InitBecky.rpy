# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label InitBecky:
    python:
        knowsMC["becky"] = True
        # Initialize Becky's attributes
        GirlName = 'becky'

        RealName[GirlName] = 'Бекки'
        RealName2[GirlName] = 'Бекки'
        RealName3[GirlName] = 'Бекки'
        age_girls[GirlName] = 36
        kids[GirlName] = 5
        beauty[GirlName] = 45
        sluttiness[GirlName] = 25
        sexacts[GirlName] = 5352
        cuminside[GirlName] = 3593
        pregnancy[GirlName] = 0
        pregfather[GirlName] = ''
        ConceptionChance[GirlName] = 5
        PussyWetStart[GirlName] = 25
        virginity[GirlName] = False

        # Description and default dress
        girltextdesc[GirlName] = 'Вдова Блэнкеншип, для друзей Бекки, высокая рыжеволосая женщина с полной грудью, чуть младше сорока лет.'
        dressdefault[GirlName] = 'openworkdress'

        # Default clothing
        bradef[GirlName] = 'simplebra'
        pantiesdef[GirlName] = 'simplepanties'
        legsdef[GirlName] = 'blackstockings'
        shoesdef[GirlName] = 'simpleshoes'

        # Skills
        cooking[GirlName] = 70
        cleaning[GirlName] = 50
        waitress[GirlName] = 40

        # Job-related data
        otkroven[GirlName] = 0
        jobkitchen[GirlName] = 0
        jobcleaning[GirlName] = 0
        jobwaitress[GirlName] = 0
        Friends[GirlName] = 0
        jobHallAvail[GirlName] = 0
        jobWhoreAvail[GirlName] = 0
        jobwhore[GirlName] = 0
        jobgloryhole[GirlName] = 0

        # Custom variables
        BeckyVar['leftdances'] = 0
        BeckyVar['danceinvitehome'] = 0
        BeckyVar['visitedhome'] = 0
        BeckyVar['husbandtalk'] = 0
        BeckyVar['eddietalk'] = 0
        BeckyVar['SawIngaFuck'] = 0
        BeckyVar['IngaSexGreet'] = 0
        BeckyVar['VisitScolded'] = 0
        BeckyVar['TodayFrontSexCheck'] = 0
        BeckyVar['HomeSex'] = 0
        BeckyVar['EddieGeorg'] = 0
        BeckyVar['EddieWhoreHome'] = 0
        BeckyVar['BeckyOpenMinet'] = 0
        BeckyVar['TimesVisited'] = 0
        BeckyVar['TalkAboutEddie'] = 0
        BeckyVar['GeorgMention'] = 0
        BeckyVar['EddieIntrReact'] = 0
        BeckyVar['PriestAdvice'] = 0
        BeckyVar['GerhardBeckyTalk'] = 0
        BeckyVar['AskedEddieFuck'] = 0
        BeckyVar['EddieTryToFuck'] = 0
        BeckyVar['EddieFailures'] = 0
        BeckyVar['EddieRobbedDay'] = 0
        BeckyVar['KnowSherwood'] = 0
        BeckyVar['SherwoodSuspect'] = 0
        BeckyVar['TradeOffer'] = 0
        BeckyVar['SherwoodWarn'] = 0
        BeckyVar['AskTradeElf'] = 0
        BeckyVar['TradeOfferText'] = ''
        BeckyVar['FingalClarify'] = 0
        BeckyVar['AdmitSherwood'] = 0
        BeckyVar['RobbedByRobin'] = 0
        BeckyVar['ConsoleRobbery'] = 0
        BeckyVar['SandraKitchenVisitMonth'] = 0
        GiftPreferences[GirlName] = ["soap_001", "wild_rose_001", "pig_lard_001", "libido_tincture_001", "drink_ale_001"]

        npc_schedule_set(GirlName, [
            NPCScheduleEntry(
                location="Church",
                weekdays=[7],
                time_slots=[0, 1],
                awake=True,
                talkable=False,
                priority=340,
                label="becky_sunday_church",
            ),
            NPCScheduleEntry(
                location="TavernKitchen",
                weekdays=[1, 2, 3, 4, 6, 7],
                time_slots=[3],
                awake=True,
                talkable=True,
                condition=becky_kitchen_visit_active,
                priority=320,
                label="becky_special_kitchen_visit",
            ),
            NPCScheduleEntry(
                location="FridayDance",
                weekdays=[5],
                time_slots=[3],
                awake=True,
                talkable=True,
                priority=315,
                label="becky_friday_dance",
            ),
            NPCScheduleEntry(
                location="TavernMain",
                weekdays=[1, 2, 3, 4, 6, 7],
                time_slots=[3],
                awake=True,
                talkable=True,
                condition=becky_tavern_visit_active,
                priority=260,
                label="becky_tavern_visit",
            ),
            NPCScheduleEntry(
                location="GroceryStore",
                weekdays=[1, 2, 3, 4, 5, 6],
                time_slots=[1, 2, 3],
                awake=True,
                talkable=True,
                condition=becky_grocery_store_active,
                priority=220,
                label="becky_grocery_shift",
            ),
            NPCScheduleEntry(
                location="BeckyHome",
                weekdays=[1, 2, 3, 4, 5, 6],
                time_slots=[0],
                awake=True,
                talkable=False,
                priority=20,
                label="becky_home_awake",
            ),
            NPCScheduleEntry(
                location="BeckyHome",
                weekdays=[7],
                time_slots=[2, 3],
                awake=True,
                talkable=False,
                priority=20,
                label="becky_sunday_home_awake",
            ),
            NPCScheduleEntry(
                location="BeckyHome",
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                time_slots=[7],
                awake=False,
                talkable=False,
                priority=10,
                label="becky_home_sleep",
            ),
        ])
        npc_schedule_sync_currentloc(GirlName)

    return

init python:
    def becky_sandra_social_visit_allowed():
        return int(Friends.get("sandra", 0) or 0) >= 5

    def becky_kitchen_visit_active(month_value=None, day_value=None):
        if not becky_sandra_social_visit_allowed():
            return False
        if not becky_monthly_sandra_kitchen_visit_due(month_value, day_value):
            return False
        return str(getLocation("sandra") or "") == "TavernKitchen"

    def becky_monthly_sandra_kitchen_visit_due(month_value=None, day_value=None):
        month_now = int(month if month_value is None else month_value or 0)
        day_now = int(day if day_value is None else day_value or 0)
        if int(week or 0) == 5:
            return False
        if time != 3 or day_now != 12:
            return False
        return int(BeckyVar.get("SandraKitchenVisitMonth", 0) or 0) != month_now

    def becky_tavern_visit_active(month_value=None, day_value=None):
        week_now = int(week or 0)
        month_now = int(month if month_value is None else month_value or 0)
        day_now = int(day if day_value is None else day_value or 0)
        if week_now == 5:
            return False
        if time != 3:
            return False
        if not becky_sandra_social_visit_allowed():
            return False
        if becky_kitchen_visit_active(month_now, day_now):
            return False
        return ((day_now + month_now) % 6) == 0

    def becky_grocery_store_active(weekday_value=None, month_value=None, day_value=None):
        week_now = int(week if weekday_value is None else weekday_value or 0)
        month_now = int(month if month_value is None else month_value or 0)
        day_now = int(day if day_value is None else day_value or 0)
        if week_now == 7 or time not in (1, 2, 3):
            return False
        if becky_kitchen_visit_active(month_now, day_now):
            return False
        if becky_tavern_visit_active(month_now, day_now):
            return False
        return True

# Auto-attach .var for PeopleInfo consistency (requested)
init python:
    # Per user request: class Becky(Girl) defined in its own Init file (see game/NPC/Girls/Becky/InitBecky.rpy)
    # All data from BeckyVar (story flags, daily counters, sex history etc.) promoted to the instance.
    # .var kept for the 879+ legacy references across the project (agent.txt compat rule).
    if 'peopleInfo' not in dir() or not isinstance(peopleInfo, dict):
        peopleInfo = {}
    class Becky(Girl):
        """Becky-specific (Georgett crossover, Eddie, pregnancy, Blackwood quest hooks, home visits)."""
        def __init__(self, name="becky", **kwargs):
            super().__init__(name, **kwargs)
            if 'BeckyVar' in dir() and isinstance(BeckyVar, dict):
                self.var = BeckyVar
                self.promote_from_var(BeckyVar)
                # Promote key story fields used in IntBeckyGuest / GeorgettBeckyVisit / BeckyEvents
                for k in ("visitedhome", "HomeSex", "EddieGeorg", "TradeOfferText", "SvalnyiGreh"):
                    if k in BeckyVar:
                        self.story_flags[k] = BeckyVar[k]
    if 'becky' not in peopleInfo or not isinstance(peopleInfo.get('becky'), Becky):
        peopleInfo['becky'] = Becky(var=BeckyVar if 'BeckyVar' in dir() else {})
    else:
        if 'BeckyVar' in dir() and isinstance(BeckyVar, dict):
            peopleInfo['becky'].var = BeckyVar
    # girls list (populated here + via _register_people_lists in PeopleRuntime.rpy)
    if 'girls' not in dir() or not isinstance(girls, list):
        girls = []
    if peopleInfo.get('becky') not in girls:
        girls.append(peopleInfo['becky'])
