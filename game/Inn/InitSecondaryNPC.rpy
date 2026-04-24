default EddieVar = {}
default AlberVar = {}
default FranVar = {}
default FranBusy = {}
default DraupnirVar = {}
default MongolVar = {}
default ZimmerVar = {}
default RobinVar = {}
default RobbersHeadNameTmp = ""
default Talked = {}
default cancumdaily_npc = {}
default KnowMongol = 0
default StolenHorseDays = 0

label InitSecondaryNPC:
    python:
        Friends["Eddie"] = 0
        Friends["Alber"] = 0
        Friends["eddie"] = 0
        Friends["alber"] = 0
        Friends["fran"] = 0
        Friends["robin"] = 0
        Friends["gerhard"] = 0
        Friends["mongol"] = 0
        Friends["zimmer"] = 0
        Friends["draupnir"] = 0

        # Deterministic startup profiles for major non-team NPCs.
        npc_profiles = {
            "eddie": {
                "name": ("Эдди", "Эдди", "Эдди"),
                "age": 19,
                "loc": "GroceryStore",
                "desc": "Эдди Блэнкеншип - сын Бекки, помогает в семейной лавке.",
            },
            "alber": {
                "name": ("Альбер", "Альбера", "Альберу"),
                "age": 36,
                "loc": "WineStore",
                "desc": "Мессир Альбер Легаре - хозяин винного погребка, женат, у него большая семья.",
            },
            "fran": {
                "name": ("Франческа", "Франчески", "Франческе"),
                "age": 26,
                "loc": "EllonaTemple",
                "desc": "Франческа - жрица Эллоны в небольшом городском храме.",
            },
            "robin": {
                "name": ("Робин", "Робина", "Робину"),
                "age": 30,
                "loc": "SherwoodTravel",
                "desc": "Робин - разбойник из Шервуда.",
            },
            "gerhard": {
                "name": ("Герхард", "Герхарда", "Герхарду"),
                "age": 44,
                "loc": "Church",
                "desc": "Отец Герхард - священник городской церкви.",
            },
            "mongol": {
                "name": ("Монгол", "Монгола", "Монголу"),
                "age": 39,
                "loc": "MarketPlace",
                "desc": "Монгол - торговец лошадьми на рынке.",
            },
            "zimmer": {
                "name": ("Циммер", "Циммера", "Циммеру"),
                "age": 41,
                "loc": "CityGuard",
                "desc": "Циммер - служащий городской стражи.",
            },
            "draupnir": {
                "name": ("Драупнир", "Драупнира", "Драупниру"),
                "age": 45,
                "loc": "StolyarWorkshop",
                "desc": "Драупнир - плотник из ремесленного квартала.",
            },
        }
        for npc_key, npc_cfg in npc_profiles.items():
            n1, n2, n3 = npc_cfg["name"]
            RealName[npc_key] = n1
            RealName2[npc_key] = n2
            RealName3[npc_key] = n3
            age_girls[npc_key] = int(npc_cfg["age"])
            DateOfBirth[npc_key] = calendar_make_birth_record(age_girls[npc_key])
            kids[npc_key] = int(kids.get(npc_key, 0) or 0)
            beauty[npc_key] = int(beauty.get(npc_key, 0) or 0)
            sluttiness[npc_key] = int(sluttiness.get(npc_key, 0) or 0)
            sexacts[npc_key] = int(sexacts.get(npc_key, 0) or 0)
            cuminside[npc_key] = int(cuminside.get(npc_key, 0) or 0)
            pregnancy[npc_key] = 0
            pregfather[npc_key] = ""
            ConceptionChance[npc_key] = 0
            PussyWetStart[npc_key] = int(PussyWetStart.get(npc_key, 0) or 0)
            virginity[npc_key] = bool(virginity.get(npc_key, 0) or 0)
            girltextdesc[npc_key] = str(npc_cfg["desc"])
            dressdefault[npc_key] = str(dressdefault.get(npc_key, "") or "")
            bradef[npc_key] = str(bradef.get(npc_key, "") or "")
            pantiesdef[npc_key] = str(pantiesdef.get(npc_key, "") or "")
            legsdef[npc_key] = str(legsdef.get(npc_key, "") or "")
            shoesdef[npc_key] = str(shoesdef.get(npc_key, "") or "")
            cooking[npc_key] = int(cooking.get(npc_key, 0) or 0)
            cleaning[npc_key] = int(cleaning.get(npc_key, 0) or 0)
            waitress[npc_key] = int(waitress.get(npc_key, 0) or 0)
            otkroven[npc_key] = int(otkroven.get(npc_key, 0) or 0)
            jobkitchen[npc_key] = 0
            jobcleaning[npc_key] = 0
            jobwaitress[npc_key] = 0
            jobHallAvail[npc_key] = 0
            jobWhoreAvail[npc_key] = 0
            jobwhore[npc_key] = 0
            jobgloryhole[npc_key] = 0
            CurrentLoc[npc_key] = str(npc_cfg["loc"])
            Talked[npc_key] = int(Talked.get(npc_key, 0) or 0)
            legacy_key = npc_key.capitalize()
            Friends[legacy_key] = int(Friends.get(legacy_key, Friends.get(npc_key, 0)) or 0)
            Talked[legacy_key] = int(Talked.get(legacy_key, Talked.get(npc_key, 0)) or 0)
            knowsMC[npc_key] = npc_key not in ("fran", "mongol")

        FightLevel["legare"] = 1

        DraupnirVar["SloganAsked"] = 0
        DraupnirVar["HoleAsked"] = 0
        DraupnirVar["GloryHoleAsked"] = 0
        DraupnirVar["SoapBarrelAsked"] = 0
        DraupnirVar["MongolLockpickOrderDay"] = -1

        EddieVar["TalkedAboutWhores"] = 0
        EddieVar["SawWithGeorgett"] = 0
        EddieVar["TalkedAboutGeorgett"] = 0
        # 1 if Eddie sees you caressing Becky under the table
        EddieVar["SawMomSex"] = 0
        EddieVar["RidiculeFollow"] = 0
        EddieVar["OthersSawWithMom"] = 0
        EddieVar["WhoreVisitFreq"] = 4
        EddieVar["FingalTalk"] = 0
        EddieVar["FingalTalkDestination"] = 0
        EddieVar["FingalTalkComplain"] = 0

        # QSP source uses cancumdaily['eddie']=2 while player uses scalar cancumdaily.
        # Keep scalar player value intact and store NPC-specific value separately.
        if isinstance(cancumdaily, dict):
            cancumdaily["eddie"] = 2
        else:
            cancumdaily_npc["eddie"] = 2

        # Eddie is scoped to grocery/location systems.
        CurrentLoc["eddie"] = "GroceryStore"
        npc_schedule_set("eddie", [
            NPCScheduleEntry(
                location="GroceryStore",
                weekdays=[1, 2, 3, 4, 5, 6],
                time_slots=[0],
                awake=True,
                talkable=True,
                priority=220,
                label="eddie_grocery_morning",
            ),
            NPCScheduleEntry(
                location="BeckyHome",
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                time_slots=[1, 2, 3],
                awake=True,
                talkable=False,
                priority=20,
                label="eddie_home_day",
            ),
            NPCScheduleEntry(
                location="BeckyHome",
                weekdays=[1, 2, 3, 4, 5, 6, 7],
                time_slots=[4],
                awake=False,
                talkable=False,
                priority=10,
                label="eddie_home_sleep",
            ),
        ])
        npc_schedule_sync_currentloc("eddie")

        AlberVar["sawwithliza"] = 0
        AlberVar["talkedaboutliza"] = 0
        AlberVar["WhoreVisitFreq"] = 3
        AlberVar["hearabouthiswife"] = 0
        AlberVar["FightYouAmanda"] = 0

        FranVar["meet"] = 0
        FranVar["ellonaask"] = 0
        FranVar["graceask"] = 0
        FranVar["conchitaask"] = 0
        FranVar["dukeask"] = 0
        FranVar["starkask"] = 0
        FranVar["stateask"] = 0
        FranVar["kingask"] = 0
        FranVar["rebelask"] = 0
        FranVar["alienask"] = 0

        MongolVar["GypsyAsk"] = 0
        MongolVar["AskPriceIncr"] = 0
        MongolVar["ZimmerKnow"] = 0
        MongolVar["HorsePrice"] = 1000
        MongolVar["DiscountAsk"] = 0
        MongolVar["TheftAsk"] = 0
        MongolVar["AskSawStolen"] = 0
        MongolVar["SawStolen"] = 0
        MongolVar["WillTryToSteal"] = 0
        MongolVar["HorsesBought"] = 0
        MongolVar["StocksArrestDay"] = -1
        MongolVar["StocksSeen"] = 0
        MongolVar["StocksFoodDay"] = -1
        MongolVar["GuardGiftSent"] = 0
        MongolVar["GuardCaptainKnown"] = 0
        MongolVar["StocksReleased"] = 0
        KnowMongol = 0

        ZimmerVar["ComplainHorse"] = 0
        ZimmerVar["SherwoodStory"] = 0
        ZimmerVar["ComplainRobin"] = 0
        ZimmerVar["RobinInvestigationDay"] = 0

        RobinVar["KnowHim"] = 0
        RobinVar["KnowComplaint"] = 0
        RobinVar["KnowPlace"] = 0
        RobinVar["KnowWeapon"] = 0
        RobinVar["RobbedNum"] = 0
        RobinVar["Negotiate"] = 0
        RobinVar["KnowBigTitsVillage"] = 0
        RobinVar["MongolSafePass"] = 0
        RobinVar["MongolSafePassUsed"] = 0
        RobinVar["KunidellOpened"] = 0
        RobinVar["KunidellDeliveries"] = 0

    $ FranBusy[0] = 0
    $ FranBusy[1] = 0
    $ FranBusy[2] = 0
    $ FranBusy[3] = 0
    $ FranBusy[4] = 0
    $ StolenHorseDays = 0

    return
