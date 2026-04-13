# NextDay_TavernDaily.rpy
# Converted from NextDay_TavernDaily.txt
# Handles daily tavern resource and event logic

label NextDay_TavernDaily():
    call SetTavernServiceLevels
    python:
        # Daily visitors and happiness
        CurDay['happy'] = 0
        CurDay['visitors'] = tavernvisitors + renpy.random.randint(-4, 4)
        if week == 5:
            CurDay['visitors'] = CurDay['visitors'] // 2
        if week == 7:
            CurDay['visitors'] = CurDay['visitors'] * 3 // 4
        if renpy.random.randint(1, 15) == 1:
            ExtraEvents += 'В гавань зашло сразу несколько больших кораблей. Их истосковавшиеся по берегу команды ломанулись в окрестные кабаки.<br>'
            CurDay['visitors'] *= 2
        if callable(record_weekly_tavern_visitors):
            record_weekly_tavern_visitors(CurDay['visitors'])
        CurDay['wine'] = CurDay['visitors']
        CurDay['products'] = CurDay['visitors']
        if CurDay['wine'] > winenum:
            CurDay['happy'] -= 1
            CurDay['wine'] = winenum
        winenum -= CurDay['wine']
        if CurDay['products'] > productnum:
            CurDay['happy'] -= 1
            CurDay['products'] = productnum
        productnum -= CurDay['products']
        CurDay['revenue'] = 1 * CurDay['products'] + 2 * CurDay['wine']
        CurDay['dineout'] = 0
        CurDay['fameaten'] = householdmembers
        if CurDay['fameaten'] > productnum:
            CurDay['dineout'] = (CurDay['fameaten'] - productnum) * 3
            CurDay['fameaten'] = productnum
            CurDay['happy'] -= 1
        productnum -= CurDay['fameaten']
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
        if SloganFixed < 2 and renpy.random.randint(1, 3) == 1:
            CurDay['happy'] -= 1
        if get_random_girl_by_job('jobwhore') and renpy.random.randint(1, 4) == 1:
            CurDay['happy'] += 1
        if get_random_girl_by_job('jobgloryhole') and renpy.random.randint(1, 3) == 1:
            CurDay['happy'] += 1
        CurDay['loyalty'] = 0
        if week > 5 and DanceSponsor == 1:
            DanceSponsor = 0
            CurDay['loyalty'] += renpy.random.randint(3, 5)
        if CurDay['happy'] > 0 and renpy.random.randint(1, 5) <= CurDay['happy']:
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
            TotalDay['KidsMoney'] += 15 * KidsPosobie
        if MyStallion:
            TotalDay['HorseFood'] += 3
        if MongolVar['WillTryToSteal']:
            _dog_theft_result = None
            if callable(globals().get("ensure_dog_runtime")):
                ensure_dog_runtime()
            if callable(globals().get("dog_catch_delinquent_apply")) and hasattr(globals().get("dog", None), "prevents_theft") and dog.prevents_theft("horse"):
                _dog_theft_result = dog_catch_delinquent_apply("horse")
            if _dog_theft_result and bool(_dog_theft_result.get("ok", False)):
                TotalDay['HorseStolen'] = '<br>Ночью какой-то негодяй попытался увести вашего коня, но пес поднял лай, сбил вора с ног и не дал ему уйти. %s' % str(_dog_theft_result.get("text", "") or "")
                MongolVar['WillTryToSteal'] = 0
                MongolVar['TheftAsk'] = 0
                MongolVar['AskSawStolen'] = 0
                MongolVar['SawStolen'] = 0
                ZimmerVar['ComplainHorse'] = 0
            else:
                TotalDay['HorseStolen'] = '<br>НЕГОДЯИ ПОД ПОКРОВОМ НОЧИ УКРАЛИ У ВАС ВАШЕГО КОНИКА, ВАШЕГО НЕНАГЛЯДНОГО %s. УТРОМ ВЫ ОБНАРУЖИЛИ ЧТО ЗАМОК НА ВОРОТАХ КОНЮШНИ ВЗЛОМАН, А ЛОШАДИ И СЛЕД ПРОСТЫЛ. НИКТО НИЧЕГО НЕ ВИДЕЛ И НЕ СЛЫШАЛ.' % MyStallion.upper()
                MyStallion = ''
                StolenHorseDays = 14
                MongolVar['TheftAsk'] = 0
                MongolVar['AskSawStolen'] = 0
                MongolVar['SawStolen'] = 0
                ZimmerVar['ComplainHorse'] = 0
        TotalDay['whorerevenue'] = 0
        # Reset jobs
        jobwhore['georgett'] = 0
        jobgloryhole['georgett'] = 0
        jobwhore['liza'] = 0
        jobgloryhole['liza'] = 0
    call change_tomorrow_whore_job('georgett')
    call change_tomorrow_whore_job('liza')
    call change_tomorrow_hall_job('sandra')
    call change_tomorrow_hall_job('melissa')
    call change_tomorrow_hall_job('amanda')
    return
