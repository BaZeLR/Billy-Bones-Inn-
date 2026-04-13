# NextDay_NewDayEvents.rpy
# Converted from NextDay_NewDayEvents.txt
# Handles new day event logic for the simulation/visual novel

init -26 python:
    import renpy.store as store

    def _nd_ensure_dict(name):
        value = getattr(store, name, None)
        if not isinstance(value, dict):
            value = {}
            setattr(store, name, value)
        return value

    def _nd_ensure_scalar(name, default_value):
        if not hasattr(store, name):
            setattr(store, name, default_value)
        return getattr(store, name)

    def _nd_ensure_fran_busy():
        value = getattr(store, "FranBusy", {})
        if isinstance(value, list):
            converted = {}
            for i in range(len(value)):
                converted[i] = int(value[i] or 0)
            value = converted
        if not isinstance(value, dict):
            value = {}
        for slot in range(5):
            value.setdefault(slot, 0)
        setattr(store, "FranBusy", value)
        return value

label NextDay_NewDayEvents():
    python:
        # Defensive defaults to avoid startup KeyError on partially initialized saves.
        BeckyVar = _nd_ensure_dict("BeckyVar")
        EddieVar = _nd_ensure_dict("EddieVar")
        CurrentLoc = _nd_ensure_dict("CurrentLoc")
        AlberVar = _nd_ensure_dict("AlberVar")
        LizaVar = _nd_ensure_dict("LizaVar")
        GeorgettVar = _nd_ensure_dict("GeorgettVar")
        IngaVar = _nd_ensure_dict("IngaVar")
        AmandaVar = _nd_ensure_dict("AmandaVar")
        GiveOrgasms = _nd_ensure_dict("GiveOrgasms")
        HadSex = _nd_ensure_dict("HadSex")
        sluttiness = _nd_ensure_dict("sluttiness")
        DayLastOrgasmGiven = _nd_ensure_dict("DayLastOrgasmGiven")
        Friends = _nd_ensure_dict("Friends")
        virginity = _nd_ensure_dict("virginity")
        sexacts = _nd_ensure_dict("sexacts")
        pantiesdef = _nd_ensure_dict("pantiesdef")
        FranBusy = _nd_ensure_fran_busy()
        MongolVar = _nd_ensure_dict("MongolVar")

        retlocname = _nd_ensure_scalar("retlocname", "")
        tavernvisitors = int(_nd_ensure_scalar("tavernvisitors", 0) or 0)
        MyStallion = _nd_ensure_scalar("MyStallion", "")
        StolenHorseDays = int(_nd_ensure_scalar("StolenHorseDays", 0) or 0)
        SloganFixed = int(_nd_ensure_scalar("SloganFixed", 0) or 0)
        TavernGloryHole = int(_nd_ensure_scalar("TavernGloryHole", 0) or 0)
        week = int(_nd_ensure_scalar("week", 1) or 1)
        dayspassed = int(_nd_ensure_scalar("dayspassed", 0) or 0)

        BeckyVar.setdefault("EddieGeorg", 0)
        BeckyVar.setdefault("EddieWhoreHome", 0)
        BeckyVar.setdefault("visitedhome", 0)
        BeckyVar.setdefault("HomeSex", 0)
        BeckyVar.setdefault("husbandtalk", 0)
        BeckyVar.setdefault("GerhardBeckyTalk", 0)
        BeckyVar.setdefault("TodayFrontSexCheck", 0)
        BeckyVar.setdefault("PriestAdvice", 0)
        BeckyVar.setdefault("EddieRobbed", 0)
        BeckyVar.setdefault("EddieRobbedDay", 0)

        EddieVar.setdefault("WhoreVisitFreq", 6)
        EddieVar.setdefault("SawMomSex", 0)
        EddieVar.setdefault("TalkedAboutWhores", 0)

        CurrentLoc.setdefault("georgett", "")
        CurrentLoc.setdefault("eddie", "GroceryStore")
        AlberVar.setdefault("WhoreVisitFreq", 6)
        LizaVar.setdefault("ProstStart", 0)
        GeorgettVar.setdefault("churchgeorgettadmit", 0)
        GeorgettVar.setdefault("churchlizaadmit", 0)
        IngaVar.setdefault("Knowher", 0)
        MongolVar.setdefault("WillTryToSteal", 0)
        AmandaVar.setdefault("glorytried", 0)
        AmandaVar.setdefault("gloryscold", 0)
        AmandaVar.setdefault("glorywalkout", 0)
        AmandaVar.setdefault("glorysuck", 0)
        AmandaVar.setdefault("glorydeflower", 0)
        AmandaVar.setdefault("fucklegare", 0)
        AmandaVar.setdefault("alberfriends", 0)
        AmandaVar.setdefault("alberprohibit", 0)
        AmandaVar.setdefault("prohibitwithguys", 0)

        GiveOrgasms.setdefault("becky", 0)
        HadSex.setdefault("becky", 0)
        sluttiness.setdefault("becky", 0)
        sluttiness.setdefault("amanda", 0)
        DayLastOrgasmGiven.setdefault("becky", 0)
        Friends.setdefault("becky", 0)
        Friends.setdefault("amanda", 0)
        virginity.setdefault("amanda", 1)
        sexacts.setdefault("amanda", 0)
        pantiesdef.setdefault("liza", "")

        # --- Заканчиваем делать то, что начали в течении дня.
        if SloganFixed == 1:
            SloganFixed = 2
        if TavernGloryHole == 1:
            TavernGloryHole = 2

        # Выберем, снимет ли Эдди Жоржи себе домой сегодня.
        if BeckyVar['EddieGeorg'] > 0:
            # Сначала сбросим предыдущее состояние
            if BeckyVar['EddieWhoreHome'] in (2, 3):
                BeckyVar['EddieWhoreHome'] -= 2
            elif BeckyVar['EddieWhoreHome'] == 4:
                BeckyVar['EddieGeorg'] = max(BeckyVar['EddieGeorg'], 2)
                BeckyVar['EddieWhoreHome'] = 0
            # Теперь определим успех на сегодня, по пятницам жоржи не приходит
            if renpy.random.randint(1, EddieVar['WhoreVisitFreq']) == 1 and week != 5:
                if BeckyVar['visitedhome'] >= 5 and EddieVar['SawMomSex'] > 0 and BeckyVar['HomeSex'] > 0:
                    if renpy.random.randint(1, 10) <= 1 + BeckyVar['EddieWhoreHome'] * 5 + (3 if BeckyVar['EddieGeorg'] > 1 else 0):
                        BeckyVar['EddieWhoreHome'] = 4
                    else:
                        BeckyVar['EddieWhoreHome'] += 2
                else:
                    BeckyVar['EddieWhoreHome'] += 2
            if BeckyVar['EddieWhoreHome'] in (2, 3):
                TodaySexEvents_Add('georgett', 3, 99, 'Prostitution')
        elif EddieVar['TalkedAboutWhores'] == 1 and CurrentLoc['georgett'] == 'TavernMain':
            if renpy.random.randint(1, EddieVar['WhoreVisitFreq']) == 1 and week != 5:
                TodaySexEvents_Add('georgett', 3, 99, 'Prostitution')
        if BeckyVar['EddieWhoreHome'] == 4:
            TodaySexEvents_Add('georgett', 99, 99, 'EddieHomeVisit')

        # Визит Легаре к Лизе
        if renpy.random.randint(1, AlberVar['WhoreVisitFreq']) == 1 and week != 5 and LizaVar['ProstStart']:
            TodaySexEvents_Add('liza', 3, 99, 'Prostitution')

        if BeckyVar['husbandtalk'] == 0 and GiveOrgasms['becky'] > 0 and HadSex['becky'] > 0:
            BeckyVar['husbandtalk'] = 1
        if BeckyVar['GerhardBeckyTalk'] == 2:
            BeckyVar['GerhardBeckyTalk'] = 1
        BeckyVar['TodayFrontSexCheck'] = 0

        # К Бекки приходят любовники
        if sluttiness['becky'] >= 35 and (DayLastOrgasmGiven['becky'] + 2) <= dayspassed and BeckyVar['visitedhome'] >= 2 and week != 7:
            if sluttiness['becky'] >= 55 or renpy.random.randint(1, 2) == 1:
                TodaySexEvents_Add('becky', 99, renpy.random.randint(1, 3), 'StoreLover')
        if BeckyVar['visitedhome'] >= 7 and renpy.random.randint(1, 3) <= 2 and CheckIfEventAlreadyExist('georgett', 99) <= 0:
            TodaySexEvents_Add('becky', 99, 99, 'EddieMom')

        if week == 7:
            if BeckyVar['PriestAdvice'] > 0:
                TodaySexEvents_Add('becky', 99, 99, 'Priest')
            if GeorgettVar['churchgeorgettadmit'] > 0:
                TodaySexEvents_Add('georgett', 99, 99, 'Priest')
            if GeorgettVar['churchlizaadmit'] > 0:
                TodaySexEvents_Add('liza', 99, 99, 'Priest')
        if IngaVar['Knowher'] > 0:
            TodaySexEvents_Add('inga', 99, 99, 'Lucas')

        # Аманда
        if sluttiness['amanda'] >= 22 and TavernGloryHole == 2 and get_random_girl_by_job('jobgloryhole') == 'liza':
            if AmandaVar['glorytried'] == 0:
                if renpy.random.randint(1, 3) == 1:
                    TodaySexEvents_Add('amanda', 99, 99, 'glorytry')
            else:
                GloryChanceDecrease = 0
                if AmandaVar['gloryscold'] == 1:
                    GloryChanceDecrease += 9
                if AmandaVar['glorywalkout'] == 1:
                    GloryChanceDecrease += 3
                if AmandaVar['glorysuck'] == 1:
                    GloryChanceDecrease -= 2
                if AmandaVar['glorydeflower'] == 1:
                    GloryChanceDecrease -= 3
                if sluttiness['amanda'] >= 35:
                    GloryChanceDecrease -= 3
                if virginity['amanda'] == 0:
                    GloryChanceDecrease -= 2
                if sexacts['amanda'] > 15:
                    GloryChanceDecrease += 2
                if sexacts['amanda'] > 35:
                    GloryChanceDecrease += 3
                if sexacts['amanda'] > 50:
                    GloryChanceDecrease += 5
                if renpy.random.randint(1, max(3, 4 + GloryChanceDecrease)) == 1:
                    TodaySexEvents_Add('amanda', 99, 99, 'glorytry')
        if AmandaVar['fucklegare'] == 1 and AmandaVar['alberfriends'] >= 10 and sluttiness['amanda'] >= 35 and week != 5:
            ChanceVar = 6
            if AmandaVar['alberfriends'] >= 15:
                ChanceVar -= 1
            if sluttiness.get('alberfriends', 0) >= 50:
                ChanceVar -= 1
            if sluttiness.get('alberfriends', 0) >= 70:
                ChanceVar -= 1
            if AmandaVar['alberprohibit']:
                ChanceVar += 5
            if Friends['amanda'] >= 15:
                ChanceVar += 2
            if renpy.random.randint(1, ChanceVar) == 1:
                TodaySexEvents_Add('amanda', 3, 99, 'legarerun')
        if sexacts['amanda'] >= 5 and sluttiness['amanda'] >= 35 and week != 5:
            ChanceVar = 4
            if sluttiness['amanda'] >= 45:
                ChanceVar -= 1
            if sluttiness['amanda'] >= 55:
                ChanceVar -= 1
            if AmandaVar['prohibitwithguys']:
                ChanceVar += 5
            if renpy.random.randint(1, ChanceVar) == 1:
                TodaySexEvents_Add('amanda', 2, 99, 'lovermeet')

        # Воровство лошадки
        if MyStallion and retlocname != 'TavernStable' and StolenHorseDays == 0 and renpy.random.randint(1, 40) == 25:
            MongolVar['WillTryToSteal'] = 1

        # Бекки предлагает подзаработать
        if BeckyVar['visitedhome'] >= 5 and Friends['becky'] >= 15 and BeckyVar['EddieRobbed'] == 0 and dayspassed > 0 and renpy.random.randint(1, 6) == 1:
            if DailyEventsList_Exists('becky', 'SherwoodQuest') == 0:
                BeckyVar['EddieRobbedDay'] = dayspassed
                DailyEventsList_Add("becky", "GroceryStore", 1, ">=", 1, 9999, "SherwoodQuest", "BeckyQuestInit")

        # Keep Eddie discoverable only in grocery-related UI/schedule logic.
        CurrentLoc['eddie'] = "GroceryStore"

        # Francheska in temple (per-time-slot availability map)
        for i in range(5):
            FranBusy[i] = 1 if renpy.random.randint(1, 3) == 1 else 0

        _run_georgett_nextday_clients = 1
        _georgett_nextday_clients_max = 5
        _georgett_nextday_glory_max = tavernvisitors // 6

        _run_liza_nextday_clients = 0
        _liza_nextday_clients_max = 0
        _liza_nextday_glory_max = tavernvisitors // 6
        if LizaVar['ProstStart']:
            _run_liza_nextday_clients = 1
            _liza_nextday_clients_max = 3 + (1 if pantiesdef['liza'] == '' else 0)
    if _run_georgett_nextday_clients:
        call WhoreNextDayClients('georgett', _georgett_nextday_clients_max, _georgett_nextday_glory_max)
    if _run_liza_nextday_clients:
        call WhoreNextDayClients('liza', _liza_nextday_clients_max, _liza_nextday_glory_max)
    return
