# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# NextDay_NewDayEvents.rpy
# Converted from NextDay_NewDayEvents.txt
# Handles new day event logic for the simulation/visual novel

label NextDay_NewDayEvents(retlocname=""):
    $ renpy.dynamic("day_value", "week_value", "_georgett_work_location", "_liza_work_location", "GloryChanceDecrease", "ChanceVar")
    $ renpy.dynamic("_run_georgett_nextday_clients", "_georgett_nextday_clients_max", "_georgett_nextday_glory_max", "_run_liza_nextday_clients", "_liza_nextday_clients_max", "_liza_nextday_glory_max")
    python:
        # Domain owners carry their own defaults, including on a new game.
        Georgett.ensure_story_defaults()
        Mongol.ensure_story_defaults()

        Amanda.ensure_story_defaults()

        day_value = current_game_day()
        week_value = int(calendar_v2.week or 0)

        player.tavern_management.breakfast.today = False
        tavern_kitchen_reset_daily_hearth_state()
        crafting_release_ready_soap_batches()

        # --- Заканчиваем делать то, что начали в течении дня.
        if player.tavern_management.slogan_state == 1:
            player.tavern_management.slogan_state = 2
        if player.tavern_management.glory_hole == 1:
            player.tavern_management.glory_hole = 2

        # Выберем, снимет ли Эдди Жоржи себе домой сегодня.
        _georgett_work_location = str(people.location("georgett", week_value, 19 * 60) or "")
        _liza_work_location = str(people.location("liza", week_value, 19 * 60) or "")

        if Becky.eddie_georgett_stage > 0:
            # Сначала сбросим предыдущее состояние
            if Becky.eddie_home_visit_state in (2, 3):
                Becky.eddie_home_visit_state -= 2
            elif Becky.eddie_home_visit_state == 4:
                Becky.eddie_georgett_stage = max(Becky.eddie_georgett_stage, 2)
                Becky.eddie_home_visit_state = 0
            # Теперь определим успех на сегодня, по пятницам жоржи не приходит
            if procedural_randint(1, Eddie.whore_visit_frequency, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:93:1") == 1 and week_value != 5:
                if Becky.home_visit_stage >= 5 and Eddie.saw_mother_sex and Becky.home_sex_unlocked:
                    if procedural_randint(1, 10, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:95:2") <= 1 + Becky.eddie_home_visit_state * 5 + (3 if Becky.eddie_georgett_stage > 1 else 0):
                        Becky.eddie_home_visit_state = 4
                    else:
                        Becky.eddie_home_visit_state += 2
                else:
                    Becky.eddie_home_visit_state += 2
            if Becky.eddie_home_visit_state in (2, 3) and _georgett_work_location in ("TavernMain", "PortStreets"):
                TodaySexEvents_Add('georgett', 3, 99, 'Prostitution')
        elif Eddie.told_about_tavern_whores and _georgett_work_location in ("TavernMain", "PortStreets"):
            if procedural_randint(1, Eddie.whore_visit_frequency, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:104:3") == 1 and week_value != 5:
                TodaySexEvents_Add('georgett', 3, 99, 'Prostitution')
        if Becky.eddie_home_visit_state == 4:
            TodaySexEvents_Add('georgett', 99, 99, 'EddieHomeVisit')

        # Визит Легаре к Лизе
        if procedural_randint(1, Alber.whore_visit_frequency, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:110:4") == 1 and week_value != 5 and Liza.prostitution_started and _liza_work_location == "PortStreets":
            TodaySexEvents_Add('liza', 3, 99, 'Prostitution')

        if Becky.gerhard_talk_stage == 2:
            Becky.gerhard_talk_stage = 1
        Becky.home_front_checked_today = False

        # К Бекки приходят любовники
        if Becky.corruption >= 35 and (Becky.last_store_orgasm_day + 2) <= day_value and Becky.home_visit_stage >= 2 and week_value != 7:
            if Becky.corruption >= 55 or procedural_randint(1, 2, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:122:5") == 1:
                TodaySexEvents_Add('becky', 99, procedural_randint(1, 3, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:123:6"), 'StoreLover')
        if Becky.home_visit_stage >= 7 and procedural_randint(1, 3, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:124:7") <= 2 and CheckIfEventAlreadyExist('georgett', 99) <= 0:
            TodaySexEvents_Add('becky', 99, 99, 'EddieMom')

        if week_value == 7:
            if Becky.can_trigger_after_sermon_event():
                TodaySexEvents_Add('becky', 99, 99, 'Priest')
            if Georgett.can_trigger_after_sermon_event():
                TodaySexEvents_Add('georgett', 99, 99, 'Priest')
            if Liza.can_trigger_after_sermon_event():
                TodaySexEvents_Add('liza', 99, 99, 'Priest')
        if Inga.acquaintance_stage > 0:
            TodaySexEvents_Add('inga', 99, 99, 'Lucas')

        # Аманда
        if Amanda.corruption >= 22 and player.tavern_management.glory_hole == 2 and get_random_girl_by_job('jobgloryhole') == 'liza':
            if Amanda.var_int("glorytried", 0) == 0:
                if procedural_randint(1, 3, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:140:8") == 1:
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
                if not bool(Amanda.sex_stat("virginity", True)):
                    GloryChanceDecrease -= 2
                if Amanda.sex_stat("sexacts", 0) > 15:
                    GloryChanceDecrease += 2
                if Amanda.sex_stat("sexacts", 0) > 35:
                    GloryChanceDecrease += 3
                if Amanda.sex_stat("sexacts", 0) > 50:
                    GloryChanceDecrease += 5
                if procedural_randint(1, max(3, 4 + GloryChanceDecrease), key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:162:9") == 1:
                    TodaySexEvents_Add('amanda', 99, 99, 'glorytry')
        if Amanda.had_sex_with_legare and Amanda.legare_affection >= 10 and Amanda.corruption >= 35 and week_value != 5:
            ChanceVar = 6
            if Amanda.legare_affection >= 15:
                ChanceVar -= 1
            if Amanda.legare_affection >= 18:
                ChanceVar -= 1
            if Amanda.legare_affection >= 20:
                ChanceVar -= 1
            if Amanda.legare_forbidden:
                ChanceVar += 5
            if Amanda.rel >= 15:
                ChanceVar += 2
            if procedural_randint(1, ChanceVar, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:176:10") == 1:
                TodaySexEvents_Add('amanda', 3, 99, 'legarerun')
        if int(Amanda.stats.get("sexacts", 0) or 0) >= 5 and Amanda.corruption >= 35 and week_value != 5:
            ChanceVar = 4
            if Amanda.corruption >= 45:
                ChanceVar -= 1
            if Amanda.corruption >= 55:
                ChanceVar -= 1
            if Amanda.var_int("prohibitwithguys", 0):
                ChanceVar += 5
            if procedural_randint(1, ChanceVar, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:186:11") == 1:
                TodaySexEvents_Add('amanda', 2, 99, 'lovermeet')

        # Воровство лошадки
        if player.horse.owns_horse() and retlocname != 'TavernStable' and player.horse.stolen_days == 0 and procedural_randint(1, 40, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:190:12") == 25:
            Mongol.will_try_to_steal = True

        # Бекки предлагает подзаработать
        if Becky.home_visit_stage >= 5 and Becky.rel >= 15 and Becky.eddie_robbed_day == 0 and day_value > 0 and procedural_randint(1, 6, key="procedural:Utilities/Time/NextDay_NewDayEvents.rpy:procedural_randint:194:13") == 1:
            if daily_events.exists('becky', 'SherwoodQuest') == 0:
                Becky.eddie_robbed_day = day_value
                daily_events.add("becky", "GroceryStore", 1, ">=", 1, 9999, "SherwoodQuest", "BeckyQuestInit", "none")

        # Francheska's exact-hour daily schedule is derived anew for the new day.
        FranStaticData.invalidate_daily_schedule()

        _run_georgett_nextday_clients = 1
        _georgett_nextday_clients_max = 5
        _georgett_nextday_glory_max = player.tavern_management.visitors // 6

        _run_liza_nextday_clients = 0
        _liza_nextday_clients_max = 0
        _liza_nextday_glory_max = player.tavern_management.visitors // 6
        if Liza.prostitution_started:
            _run_liza_nextday_clients = 1
            _liza_nextday_clients_max = 3 + (1 if Liza.current_underwear("panties", "") == "" else 0)
    if _run_georgett_nextday_clients:
        call WhoreNextDayClients('georgett', _georgett_nextday_clients_max, _georgett_nextday_glory_max)
    if _run_liza_nextday_clients:
        call WhoreNextDayClients('liza', _liza_nextday_clients_max, _liza_nextday_glory_max)
    return
