# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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
        IngaVar = _nd_ensure_dict("IngaVar")
        GiveOrgasms = _nd_ensure_dict("GiveOrgasms")
        DayLastOrgasmGiven = _nd_ensure_dict("DayLastOrgasmGiven")
        virginity = _nd_ensure_dict("virginity")
        sexacts = _nd_ensure_dict("sexacts")
        pantiesdef = _nd_ensure_dict("pantiesdef")
        FranBusy = _nd_ensure_fran_busy()
        Georgett.ensure_story_defaults()
        Liza.ensure_story_defaults()
        Mongol.ensure_story_defaults()

        retlocname = _nd_ensure_scalar("retlocname", "")
        tavernvisitors = int(_nd_ensure_scalar("tavernvisitors", 40) or 0)
        MyStallion = _nd_ensure_scalar("MyStallion", "")
        StolenHorseDays = int(_nd_ensure_scalar("StolenHorseDays", 0) or 0)
        SloganFixed = int(_nd_ensure_scalar("SloganFixed", 0) or 0)
        TavernGloryHole = int(_nd_ensure_scalar("TavernGloryHole", 0) or 0)
        week = int(_nd_ensure_scalar("week", 1) or 1)
        dayspassed = int(_nd_ensure_scalar("dayspassed", 0) or 0)
        _nd_ensure_scalar("BreakfastToday", False)

        Eddie.ensure_story_defaults()

        Alber.ensure_story_defaults()
        IngaVar.setdefault("Knowher", 0)
        Amanda.ensure_story_defaults()

        virginity.setdefault("amanda", 1)
        sexacts.setdefault("amanda", 0)
        pantiesdef.setdefault("liza", "")
        store.BreakfastToday = False
        tavern_kitchen_reset_daily_hearth_state()

        # --- Заканчиваем делать то, что начали в течении дня.
        if SloganFixed == 1:
            SloganFixed = 2
        if TavernGloryHole == 1:
            TavernGloryHole = 2

        # Выберем, снимет ли Эдди Жоржи себе домой сегодня.
        _georgett_work_location = str(getLocation("georgett", week, 19 * 60) or "")
        _liza_work_location = str(getLocation("liza", week, 19 * 60) or "")

        Becky.ensure_story_defaults()
        _becky_story = Becky.var
        if _becky_story['EddieGeorg'] > 0:
            # Сначала сбросим предыдущее состояние
            if _becky_story['EddieWhoreHome'] in (2, 3):
                _becky_story['EddieWhoreHome'] -= 2
            elif _becky_story['EddieWhoreHome'] == 4:
                _becky_story['EddieGeorg'] = max(_becky_story['EddieGeorg'], 2)
                _becky_story['EddieWhoreHome'] = 0
            # Теперь определим успех на сегодня, по пятницам жоржи не приходит
            if renpy.random.randint(1, Eddie.var['WhoreVisitFreq']) == 1 and week != 5:
                if _becky_story['visitedhome'] >= 5 and Eddie.var['SawMomSex'] > 0 and _becky_story['HomeSex'] > 0:
                    if renpy.random.randint(1, 10) <= 1 + _becky_story['EddieWhoreHome'] * 5 + (3 if _becky_story['EddieGeorg'] > 1 else 0):
                        _becky_story['EddieWhoreHome'] = 4
                    else:
                        _becky_story['EddieWhoreHome'] += 2
                else:
                    _becky_story['EddieWhoreHome'] += 2
            if _becky_story['EddieWhoreHome'] in (2, 3) and _georgett_work_location in ("TavernMain", "PortStreets"):
                TodaySexEvents_Add('georgett', 3, 99, 'Prostitution')
        elif Eddie.var['TalkedAboutWhores'] == 1 and _georgett_work_location in ("TavernMain", "PortStreets"):
            if renpy.random.randint(1, Eddie.var['WhoreVisitFreq']) == 1 and week != 5:
                TodaySexEvents_Add('georgett', 3, 99, 'Prostitution')
        if Becky.var['EddieWhoreHome'] == 4:
            TodaySexEvents_Add('georgett', 99, 99, 'EddieHomeVisit')

        # Визит Легаре к Лизе
        if renpy.random.randint(1, Alber.var_int("WhoreVisitFreq", 3)) == 1 and week != 5 and Liza.story_value("ProstStart", 0) and _liza_work_location == "PortStreets":
            TodaySexEvents_Add('liza', 3, 99, 'Prostitution')

        Becky.ensure_story_defaults()
        if Becky.var['husbandtalk'] == 0 and Becky.stats.get("orgasms_given", 0) > 0 and Becky.stats.get("sexacts", 0) > 0:
            Becky.var['husbandtalk'] = 1
        if Becky.var['GerhardBeckyTalk'] == 2:
            Becky.var['GerhardBeckyTalk'] = 1
        Becky.var['TodayFrontSexCheck'] = 0

        # К Бекки приходят любовники
        if Becky.corruption >= 35 and (Becky.story_value("last_store_orgasm_day", -1) + 2) <= dayspassed and Becky.var['visitedhome'] >= 2 and week != 7:
            if Becky.corruption >= 55 or renpy.random.randint(1, 2) == 1:
                TodaySexEvents_Add('becky', 99, renpy.random.randint(1, 3), 'StoreLover')
        if Becky.var['visitedhome'] >= 7 and renpy.random.randint(1, 3) <= 2 and CheckIfEventAlreadyExist('georgett', 99) <= 0:
            TodaySexEvents_Add('becky', 99, 99, 'EddieMom')

        if week == 7:
            if Becky.var['PriestAdvice'] > 0:
                TodaySexEvents_Add('becky', 99, 99, 'Priest')
            if Georgett.can_trigger_after_sermon_event():
                TodaySexEvents_Add('georgett', 99, 99, 'Priest')
            if Liza.can_trigger_church_service_event():
                TodaySexEvents_Add('liza', 99, 99, 'Priest')
        if IngaVar['Knowher'] > 0:
            TodaySexEvents_Add('inga', 99, 99, 'Lucas')

        # Аманда
        if Amanda.corruption >= 22 and TavernGloryHole == 2 and get_random_girl_by_job('jobgloryhole') == 'liza':
            if Amanda.var_int("glorytried", 0) == 0:
                if renpy.random.randint(1, 3) == 1:
                    TodaySexEvents_Add('amanda', 99, 99, 'glorytry')
            else:
                GloryChanceDecrease = 0
                if Amanda.var_int("gloryscold", 0) == 1:
                    GloryChanceDecrease += 9
                if Amanda.var_int("glorywalkout", 0) == 1:
                    GloryChanceDecrease += 3
                if Amanda.var_int("glorysuck", 0) == 1:
                    GloryChanceDecrease -= 2
                if Amanda.var_int("glorydeflower", 0) == 1:
                    GloryChanceDecrease -= 3
                if Amanda.corruption >= 35:
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
        if Amanda.var_int("fucklegare", 0) == 1 and Amanda.var_int("alberfriends", 0) >= 10 and Amanda.corruption >= 35 and week != 5:
            ChanceVar = 6
            if Amanda.var_int("alberfriends", 0) >= 15:
                ChanceVar -= 1
            if Amanda.var_int("alberfriends", 0) >= 18:
                ChanceVar -= 1
            if Amanda.var_int("alberfriends", 0) >= 20:
                ChanceVar -= 1
            if Amanda.var_int("alberprohibit", 0):
                ChanceVar += 5
            if Amanda.rel >= 15:
                ChanceVar += 2
            if renpy.random.randint(1, ChanceVar) == 1:
                TodaySexEvents_Add('amanda', 3, 99, 'legarerun')
        if int(Amanda.stats.get("sexacts", 0) or 0) >= 5 and Amanda.corruption >= 35 and week != 5:
            ChanceVar = 4
            if Amanda.corruption >= 45:
                ChanceVar -= 1
            if Amanda.corruption >= 55:
                ChanceVar -= 1
            if Amanda.var_int("prohibitwithguys", 0):
                ChanceVar += 5
            if renpy.random.randint(1, ChanceVar) == 1:
                TodaySexEvents_Add('amanda', 2, 99, 'lovermeet')

        # Воровство лошадки
        if MyStallion and retlocname != 'TavernStable' and StolenHorseDays == 0 and renpy.random.randint(1, 40) == 25:
            Mongol.var['WillTryToSteal'] = 1

        # Бекки предлагает подзаработать
        if Becky.var['visitedhome'] >= 5 and Becky.rel >= 15 and Becky.var['EddieRobbed'] == 0 and dayspassed > 0 and renpy.random.randint(1, 6) == 1:
            if DailyEventsList_Exists('becky', 'SherwoodQuest') == 0:
                Becky.var['EddieRobbedDay'] = dayspassed
                DailyEventsList_Add("becky", "GroceryStore", 1, ">=", 1, 9999, "SherwoodQuest", "BeckyQuestInit")

        # Francheska in temple (per-time-slot availability map)
        for i in range(5):
            FranBusy[i] = 1 if renpy.random.randint(1, 3) == 1 else 0

        _run_georgett_nextday_clients = 1
        _georgett_nextday_clients_max = 5
        _georgett_nextday_glory_max = tavernvisitors // 6

        _run_liza_nextday_clients = 0
        _liza_nextday_clients_max = 0
        _liza_nextday_glory_max = tavernvisitors // 6
        if Liza.story_value("ProstStart", 0):
            _run_liza_nextday_clients = 1
            _liza_nextday_clients_max = 3 + (1 if pantiesdef['liza'] == '' else 0)
        npc_schedule_sync_all()
        werecat_sync_profile()
    if _run_georgett_nextday_clients:
        call WhoreNextDayClients('georgett', _georgett_nextday_clients_max, _georgett_nextday_glory_max)
    if _run_liza_nextday_clients:
        call WhoreNextDayClients('liza', _liza_nextday_clients_max, _liza_nextday_glory_max)
    return
