# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# NextDay_TavernDaily.rpy
# Converted from NextDay_TavernDaily.txt
# Handles daily tavern resource and event logic

label NextDay_TavernDaily():
    $ renpy.dynamic("_dog_theft_result", "_kitchen_effect_lines", "_kitchen_stock_used", "_rat_food_loss_due_day")
    call SetTavernServiceLevels
    python:
        # Daily visitors and happiness
        CurDay['happy'] = 0
        CurDay['visitors'] = player.tavern_management.visitors + procedural_randint(-4, 4, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:13:1")
        if int(calendar_v2.week or 0) == 5:
            CurDay['visitors'] = CurDay['visitors'] // 2
        if int(calendar_v2.week or 0) == 7:
            CurDay['visitors'] = 0
        if procedural_randint(1, 15, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:18:2") == 1:
            ExtraEvents += 'В гавань зашло сразу несколько больших кораблей. Их истосковавшиеся по берегу команды ломанулись в окрестные кабаки.<br>'
            CurDay['visitors'] *= 2
        record_weekly_tavern_visitors(CurDay['visitors'])
        CurDay['wine'] = CurDay['visitors']
        CurDay['products'] = CurDay['visitors']
        CurDay['kitchen_stock_used'] = 0
        _kitchen_stock_used = tavern_kitchen_daily_product_savings(CurDay['products'])
        CurDay['kitchen_stock_used'] = _kitchen_stock_used
        CurDay['products'] = max(0, CurDay['products'] - _kitchen_stock_used)
        if tavern_kitchen_boar_bonus_active():
            CurDay['wine'] = max(0, (CurDay['wine'] * 105 + 99) // 100)
        if CurDay['wine'] > player.tavern_management.winenum:
            CurDay['happy'] -= 1
            CurDay['wine'] = player.tavern_management.winenum
        player.tavern_management.winenum -= CurDay['wine']
        if CurDay['products'] > player.tavern_management.productnum:
            CurDay['happy'] -= 1
            CurDay['products'] = player.tavern_management.productnum
        player.tavern_management.productnum -= CurDay['products']
        CurDay['revenue'] = round((CurDay['products'] * 8 + CurDay['wine'] * 30) * 0.1, 2)
        if tavern_kitchen_boar_bonus_active():
            CurDay['revenue'] = round(CurDay['revenue'] * 1.15, 2)
        _kitchen_effect_lines = tavern_kitchen_apply_daily_food_effects()
        if len(list(_kitchen_effect_lines or [])) > 0:
            ExtraEvents += "{b}" + "\n".join(list(_kitchen_effect_lines or [])) + "{/b}\n"
        CurDay['dineout'] = 0
        CurDay['fameaten'] = player.tavern_management.household_members
        CurDay['rat_food_loss'] = 0
        if CurDay['fameaten'] > player.tavern_management.productnum:
            CurDay['dineout'] = (CurDay['fameaten'] - player.tavern_management.productnum) * 3
            CurDay['fameaten'] = player.tavern_management.productnum
            CurDay['happy'] -= 1
        player.tavern_management.productnum -= CurDay['fameaten']
        _rat_food_loss_due_day = int(werecat_state().get('rat_food_loss_next_day', -1) or -1)
        if int(werecat_state().get('rats_problem_active', 0) or 0) == 1 and _rat_food_loss_due_day >= 0 and int(current_game_day()) >= _rat_food_loss_due_day:
            CurDay['rat_food_loss'] = min(3, int(player.tavern_management.productnum or 0))
            player.tavern_management.productnum = max(0, int(player.tavern_management.productnum or 0) - CurDay['rat_food_loss'])
            werecat_state()['rat_food_loss_next_day'] = int(current_game_day()) + 7
            if CurDay['rat_food_loss'] == 1:
                ExtraEvents += '{b}Крысы снова добрались до кладовой и испортили 1 мешок припасов.{/b}\n'
            elif CurDay['rat_food_loss'] == 2:
                ExtraEvents += '{b}Крысы снова добрались до кладовой и испортили 2 мешка припасов.{/b}\n'
            elif CurDay['rat_food_loss'] >= 3:
                ExtraEvents += '{b}Крысы снова добрались до кладовой и испортили 3 мешка припасов.{/b}\n'
            else:
                ExtraEvents += '{b}Крысы опять шуршали в кладовой, но брать там уже почти нечего.{/b}\n'
        CurDay['fixedcost'] = player.tavern_management.household_members * 1 + 10
        # Service level effects
        if CurDay['happy'] >= 0:
            if player.tavern_management.service.waitress_score < 10 or player.tavern_management.service.cleanliness_score < 10 or player.tavern_management.service.kitchen_score < 10:
                CurDay['happy'] -= 1
            else:
                tavernlevel = player.tavern_management.service.waitress_score + player.tavern_management.service.cleanliness_score + player.tavern_management.service.kitchen_score
                if tavernlevel > CurDay['visitors'] * 4:
                    CurDay['happy'] += 1
        # Sign and girls effects
        if player.tavern_management.slogan_state < 2 and procedural_randint(1, 3, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:76:3") == 1:
            CurDay['happy'] -= 1
        if get_random_girl_by_job('jobwhore') and procedural_randint(1, 4, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:78:4") == 1:
            CurDay['happy'] += 1
        if get_random_girl_by_job('jobgloryhole') and procedural_randint(1, 3, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:80:5") == 1:
            CurDay['happy'] += 1
        CurDay['loyalty'] = 0
        if int(calendar_v2.week or 0) > 5 and player.tavern_management.dance_sponsor == 1:
            player.tavern_management.dance_sponsor = 0
            CurDay['loyalty'] += procedural_randint(3, 5, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:85:6")
        if CurDay['happy'] > 0 and procedural_randint(1, 5, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:86:7") <= CurDay['happy']:
            CurDay['loyalty'] += 1
        if CurDay['happy'] < 0:
            CurDay['loyalty'] += CurDay['happy']
        # Add to totals
        TotalDay['visitors'] += CurDay['visitors']
        TotalDay['wine'] += CurDay['wine']
        TotalDay['products'] += CurDay['products']
        TotalDay['revenue'] += CurDay['revenue']
        TotalDay['fameaten'] += CurDay['fameaten']
        TotalDay['dineout'] += CurDay['dineout']
        TotalDay['fixedcost'] += CurDay['fixedcost']
        TotalDay['happy'] += CurDay['happy']
        TotalDay['loyalty'] += CurDay['loyalty']
        if int(calendar_v2.week or 0) == 7:
            TotalDay['KidsMoney'] += player.economy.weekly_child_support_money()
        if player.horse.owns_horse():
            TotalDay['HorseFood'] += 3
        if Mongol.will_try_to_steal:
            _dog_theft_result = None
            if dog.prevents_theft("horse"):
                _dog_theft_result = dog_catch_delinquent_apply("horse")
            if _dog_theft_result and bool(_dog_theft_result.get("ok", False)):
                TotalDay['HorseStolen'] = '{b}Ночью какой-то негодяй попытался увести вашего коня, но пес поднял лай, сбил вора с ног и не дал ему уйти. %s{/b}\n' % str(_dog_theft_result.get("text", "") or "")
                Mongol.will_try_to_steal = False
                Mongol.theft_asked = False
                Mongol.asked_about_seen_stolen = False
                Mongol.seen_with_stolen_horse = False
                Zimmer.horse_complaint_stage = 0
            else:
                TotalDay['HorseStolen'] = '{b}НЕГОДЯИ ПОД ПОКРОВОМ НОЧИ УКРАЛИ У ВАС ВАШЕГО КОНИКА, ВАШЕГО НЕНАГЛЯДНОГО %s. УТРОМ ВЫ ОБНАРУЖИЛИ ЧТО ЗАМОК НА ВОРОТАХ КОНЮШНИ ВЗЛОМАН, А ЛОШАДИ И СЛЕД ПРОСТЫЛ. НИКТО НИЧЕГО НЕ ВИДЕЛ И НЕ СЛЫШАЛ.{/b}\n' % player.horse.name.upper()
                player.horse.mark_stolen(14)
                Mongol.theft_asked = False
                Mongol.asked_about_seen_stolen = False
                Mongol.seen_with_stolen_horse = False
                Zimmer.horse_complaint_stage = 0
        TotalDay['whorerevenue'] = 0
        # Reset jobs
        Georgett.set_job_value("jobwhore", 0)
        Georgett.set_job_value("jobgloryhole", 0)
        Liza.reset_tavern_work_day()
    $ change_tomorrow_whore_job('georgett')
    $ change_tomorrow_whore_job('liza')
    $ apply_tomorrow_hall_job('sandra')
    $ apply_tomorrow_hall_job('melissa')
    $ apply_tomorrow_hall_job('amanda')
    return


