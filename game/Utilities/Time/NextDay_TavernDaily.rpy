# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# NextDay_TavernDaily.rpy
# Converted from NextDay_TavernDaily.txt
# Handles daily tavern resource and event logic

label NextDay_TavernDaily():
    call SetTavernServiceLevels
    python:
        # Daily visitors and happiness
        CurDay['happy'] = 0
        CurDay['visitors'] = tavernvisitors + procedural_randint(-4, 4, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:13:1")
        if week == 5:
            CurDay['visitors'] = CurDay['visitors'] // 2
        if week == 7:
            CurDay['visitors'] == 0
        if procedural_randint(1, 15, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:18:2") == 1:
            ExtraEvents += 'В гавань зашло сразу несколько больших кораблей. Их истосковавшиеся по берегу команды ломанулись в окрестные кабаки.<br>'
            CurDay['visitors'] *= 2
        if callable(record_weekly_tavern_visitors):
            record_weekly_tavern_visitors(CurDay['visitors'])
        CurDay['wine'] = CurDay['visitors']
        CurDay['products'] = CurDay['visitors']
        CurDay['kitchen_stock_used'] = 0
        _kitchen_stock_used = tavern_kitchen_daily_product_savings(CurDay['products'])
        CurDay['kitchen_stock_used'] = _kitchen_stock_used
        CurDay['products'] = max(0, CurDay['products'] - _kitchen_stock_used)
        if tavern_kitchen_boar_bonus_active():
            CurDay['wine'] = max(0, (CurDay['wine'] * 105 + 99) // 100)
        if CurDay['wine'] > winenum:
            CurDay['happy'] -= 1
            CurDay['wine'] = winenum
        winenum -= CurDay['wine']
        if CurDay['products'] > productnum:
            CurDay['happy'] -= 1
            CurDay['products'] = productnum
        productnum -= CurDay['products']
        CurDay['revenue'] = round((CurDay['products'] * 8 + CurDay['wine'] * 30) * 0.1, 2)
        if tavern_kitchen_boar_bonus_active():
            CurDay['revenue'] = round(CurDay['revenue'] * 1.15, 2)
        _kitchen_effect_lines = tavern_kitchen_apply_daily_food_effects()
        if len(list(_kitchen_effect_lines or [])) > 0:
            ExtraEvents += "{b}" + "\n".join(list(_kitchen_effect_lines or [])) + "{/b}\n"
        CurDay['dineout'] = 0
        CurDay['fameaten'] = householdmembers
        CurDay['rat_food_loss'] = 0
        if CurDay['fameaten'] > productnum:
            CurDay['dineout'] = (CurDay['fameaten'] - productnum) * 3
            CurDay['fameaten'] = productnum
            CurDay['happy'] -= 1
        productnum -= CurDay['fameaten']
        _rat_food_loss_due_day = int(werecat_state().get('rat_food_loss_next_day', -1) or -1)
        if int(werecat_state().get('rats_problem_active', 0) or 0) == 1 and _rat_food_loss_due_day >= 0 and int(dayspassed or 0) >= _rat_food_loss_due_day:
            CurDay['rat_food_loss'] = min(3, int(productnum or 0))
            productnum = max(0, int(productnum or 0) - CurDay['rat_food_loss'])
            werecat_state()['rat_food_loss_next_day'] = int(dayspassed or 0) + 7
            if CurDay['rat_food_loss'] == 1:
                ExtraEvents += '{b}Крысы снова добрались до кладовой и испортили 1 мешок припасов.{/b}\n'
            elif CurDay['rat_food_loss'] == 2:
                ExtraEvents += '{b}Крысы снова добрались до кладовой и испортили 2 мешка припасов.{/b}\n'
            elif CurDay['rat_food_loss'] >= 3:
                ExtraEvents += '{b}Крысы снова добрались до кладовой и испортили 3 мешка припасов.{/b}\n'
            else:
                ExtraEvents += '{b}Крысы опять шуршали в кладовой, но брать там уже почти нечего.{/b}\n'
        CurDay['fixedcost'] = householdmembers * 1 + 10
        # Service level effects
        if CurDay['happy'] >= 0:
            if tavernwaitress_value < 10 or tavernclean_value < 10 or tavernkitchen_value < 10:
                CurDay['happy'] -= 1
            else:
                tavernlevel = tavernwaitress_value + tavernclean_value + tavernkitchen_value
                if tavernlevel > CurDay['visitors'] * 4:
                    CurDay['happy'] += 1
        # Sign and girls effects
        if SloganFixed < 2 and procedural_randint(1, 3, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:76:3") == 1:
            CurDay['happy'] -= 1
        if get_random_girl_by_job('jobwhore') and procedural_randint(1, 4, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:78:4") == 1:
            CurDay['happy'] += 1
        if get_random_girl_by_job('jobgloryhole') and procedural_randint(1, 3, key="procedural:Utilities/Time/NextDay_TavernDaily.rpy:procedural_randint:80:5") == 1:
            CurDay['happy'] += 1
        CurDay['loyalty'] = 0
        if week > 5 and DanceSponsor == 1:
            DanceSponsor = 0
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
        if week == 7:
            TotalDay['KidsMoney'] += player_state().economy.weekly_child_support_money()
        if MyStallion:
            TotalDay['HorseFood'] += 3
        if Mongol.var['WillTryToSteal']:
            _dog_theft_result = None
            try:
                ensure_dog_runtime()
            except Exception:
                pass
            try:
                _dog_guard = dog
            except Exception:
                _dog_guard = None
            try:
                _dog_catch_apply = dog_catch_delinquent_apply
            except Exception:
                _dog_catch_apply = None
            if callable(_dog_catch_apply) and hasattr(_dog_guard, "prevents_theft") and _dog_guard.prevents_theft("horse"):
                _dog_theft_result = dog_catch_delinquent_apply("horse")
            if _dog_theft_result and bool(_dog_theft_result.get("ok", False)):
                TotalDay['HorseStolen'] = '{b}Ночью какой-то негодяй попытался увести вашего коня, но пес поднял лай, сбил вора с ног и не дал ему уйти. %s{/b}\n' % str(_dog_theft_result.get("text", "") or "")
                Mongol.var['WillTryToSteal'] = 0
                Mongol.var['TheftAsk'] = 0
                Mongol.var['AskSawStolen'] = 0
                Mongol.var['SawStolen'] = 0
                Zimmer.var['ComplainHorse'] = 0
            else:
                TotalDay['HorseStolen'] = '{b}НЕГОДЯИ ПОД ПОКРОВОМ НОЧИ УКРАЛИ У ВАС ВАШЕГО КОНИКА, ВАШЕГО НЕНАГЛЯДНОГО %s. УТРОМ ВЫ ОБНАРУЖИЛИ ЧТО ЗАМОК НА ВОРОТАХ КОНЮШНИ ВЗЛОМАН, А ЛОШАДИ И СЛЕД ПРОСТЫЛ. НИКТО НИЧЕГО НЕ ВИДЕЛ И НЕ СЛЫШАЛ.{/b}\n' % MyStallion.upper()
                MyStallion = ''
                HorsePurchasePrice = 0
                StolenHorseDays = 14
                Mongol.var['TheftAsk'] = 0
                Mongol.var['AskSawStolen'] = 0
                Mongol.var['SawStolen'] = 0
                Zimmer.var['ComplainHorse'] = 0
        TotalDay['whorerevenue'] = 0
        # Reset jobs
        jobwhore['georgett'] = 0
        jobgloryhole['georgett'] = 0
        Liza.reset_tavern_work_day()
    call change_tomorrow_whore_job('georgett')
    call change_tomorrow_whore_job('liza')
    call change_tomorrow_hall_job('sandra')
    call change_tomorrow_hall_job('melissa')
    call change_tomorrow_hall_job('amanda')
    return
