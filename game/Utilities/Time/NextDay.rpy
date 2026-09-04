# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# NextDay location - converted from legacy script
init python:
    class NextDayRuntimeState(object):
        def __init__(self):
            self.report_title = ""
            self.report_body = ""
            self.current_day = {}

        def update(self):
            self.report_title = str(getattr(self, "report_title", "") or "")
            self.report_body = str(getattr(self, "report_body", "") or "")
            current_day = getattr(self, "current_day", {})
            self.current_day = dict(current_day) if isinstance(current_day, dict) else {}
            return self

    def _nextday_clean_report_text(text):
        return str(text or "").replace("<br>", "\n").strip()

    def nextday_started_after_midnight():
        current_hour = int(calendar_v2.hour or 0) % 24
        return 0 <= current_hour < 6

label NextDay(retlocname, timepassed):
    $ renpy.dynamic("visitorshappy", "_nextday_skip_first_calendar_roll", "TotalEventsSummary", "ExtraEvents", "iDaysCount", "_nextday_girl", "TotalDay", "TotalWhoreClients", "TotalGloryHoleClients", "_weekly_msg", "CurDay", "_nextday_event_day_number", "_nextday_event_date", "_nextday_summary_text", "_nextday_money_delta", "NewDressCame", "dress_name", "avg_happy", "tavernlevel", "_nextday_lines", "_geo_name", "_liza_name", "_tractir_game_over_ending", "_nextday_return_label", "_day_start_save_name", "_girl")
    $ next_day_runtime.update()
    $ visitorshappy = 0
    $ _nextday_skip_first_calendar_roll = nextday_started_after_midnight()
    
    python:
        TotalEventsSummary = ''
        ExtraEvents = ''
        iDaysCount = 0
        for _nextday_girl in people.girl_values():
            _nextday_girl.reset_skill_gains()
        
        # Initialize totals dictionaries
        TotalDay = {
            'whorerevenue': 0, 'gloryholerevenue': 0, 'loyalty': 0,
            'revenue': 0, 'dineout': 0, 'fixedcost': 0, 'KidsMoney': 0,
            'visitors': 0, 'wine': 0, 'products': 0, 'HorseFood': 0,
            'HorseStolen': False, 'fameaten': 0, 'happy': 0
        }
        TotalWhoreClients = {'georgett': 0, 'liza': 0}
        TotalGloryHoleClients = {'georgett': 0, 'liza': 0}

    while iDaysCount < timepassed:
        python:
            _weekly_msg = str(evaluate_weekly_chores_and_rewards() or "")
            if _weekly_msg:
                ExtraEvents += _weekly_msg

        call NextDay_FinishDayEvents
        $ next_day_runtime.current_day = {}
        $ CurDay = next_day_runtime.current_day
        call NextDay_TavernDaily

        python:
            _nextday_event_day_number = int(calendar_v2.daysInGame or 0)
            if _nextday_skip_first_calendar_roll and iDaysCount == 0:
                _nextday_event_day_number = max(0, _nextday_event_day_number - 1)
            _nextday_event_date = calendar_v2.day_number_to_parts(_nextday_event_day_number)
        call DisplayTavernEventsSummary(_nextday_event_date["day"], _nextday_event_date["month"], _nextday_event_date["year"])
        $ _nextday_summary_text = _return
        if _nextday_summary_text:
            $ TotalEventsSummary += _nextday_summary_text
        
        if not (_nextday_skip_first_calendar_roll and iDaysCount == 0):
            python:
                calendar_v2.day += 1
                calendar_v2.week += 1
                calendar_v2.daysInGame += 1

                if calendar_v2.week > 7:
                    calendar_v2.week = 1

                if calendar_v2.day > 28:
                    calendar_v2.day = 1
                    calendar_v2.period += 1

                if calendar_v2.period > 13:
                    calendar_v2.period = 1
                    calendar_v2.cycle += 1

        $ calendar_v2.hour = 6
        $ calendar_v2.minute = 0
        $ Clara.prepare_daily_event_rolls()
        $ player.daily_maintenance(1)
        
        call NextDay_NewDayEvents(retlocname)
        call CreateTavernEvents
        
        $ iDaysCount += 1
        call stat

    # Calculate revenues
    python:
        TotalDay['whorerevenue'] = TotalWhoreClients['georgett']*3 + TotalWhoreClients['liza']*3
        TotalDay['gloryholerevenue'] = TotalGloryHoleClients['georgett']*2 + TotalGloryHoleClients['liza']*2
        
        player.economy.tavern_fame += TotalDay['loyalty']
        _nextday_money_delta = (TotalDay['revenue'] - TotalDay['dineout'] - TotalDay['fixedcost'] +
                TotalDay['whorerevenue'] + TotalDay['gloryholerevenue'] +
                TotalDay['KidsMoney'] + (600 if player.economy.child_birth_benefit_notice else 0))
        player.add_money(_nextday_money_delta)
        
        NewDressCame = ''
        
        # Handle dress delivery
        if dress_shop.produced:
            if dress_shop.buyer == 'You':
                dress_name = ShortDressName.get(dress_shop.produced, dress_shop.produced).lower()
                NewDressCame = f'Утром прибежал посыльный из лавки Фараго и принес вам ваш заказ - {dress_name}.'
                player.appearance.replace_dress(dress_shop.produced, int(current_game_day()))
                
            if player.economy.money >= 50:
                NewDressCame += f' Вы поблагодарили мальчишку, дав ему 5 мараведи, и положили обнову в ларь.'
                player.spend_money(5)
            else:
                NewDressCame += f' Вы забрали заказ, проигнорировав протянутую ладошку мальчишки и не дав ему ничего на чай. А обновку вы положили в ларь.'
                Irma.change_social(friend_delta=-1)
                
        dress_shop.produced = ''
        dress_shop.buyer = ''
        
        # Calculate tavern level based on happiness
        avg_happy = TotalDay['happy'] / float(timepassed) if timepassed else 0
        if avg_happy > 3:
            tavernlevel = 'Ваши завсегдатаи просто обожают ваш трактир!'
        elif avg_happy > 2:
            tavernlevel = 'Ваши завсегдатаи ни за что не променяют ваше заведение ни на какое другое!'
        elif avg_happy > 1:
            tavernlevel = 'Ваши посетители просто потрясены качеством работы вашего заведения!'
        elif avg_happy > 0:
            tavernlevel = 'Вашим посетителям у вас очень нравится!'
        elif avg_happy > -1:
            tavernlevel = 'Ваши посетители не находят ничего примечательного в вашем трактире. Трактир как трактир.'
        elif avg_happy > -2:
            tavernlevel = 'Вашим посетителям не очень нравится у вас. Многие говорят что рядом есть трактиры и получше.'
        elif avg_happy > -3:
            tavernlevel = 'Многие из зашедших в ваш трактир перед уходом громогласно заявляют, что "Сюда больше ни ногой!".'
        else:
            tavernlevel = 'Даже затруднительно сказать, что больше отпугивает посетителей - непролазная грязь, отвратительное обслуживание или несъедобная еда?'

    python:
        _nextday_lines = []
        _geo_name = str(people_display_name('georgett') or 'Жоржетта')
        _liza_name = str(people_display_name('liza') or 'Лизетта')

        _nextday_lines.append("Новый день настал!")

        if str(ExtraEvents or "").strip():
            _nextday_lines.append(_nextday_clean_report_text(ExtraEvents))

        _nextday_lines.append("За прошедшее время у вас побывало %s посетителей." % TotalDay['visitors'])
        _nextday_lines.append("Они выпили %s бочонков вина." % DispFrac(TotalDay['wine']))
        _nextday_lines.append("На их еду кухня потратила %s мешков продуктов." % DispFrac(TotalDay['products']))
        _nextday_lines.append("Они заплатили вам %s мараведи." % TotalDay['revenue'])
        _nextday_lines.append("Затраты на налоги, дрова, и прочие мелкие расходы, а также карманные деньги вашим домочадцам составили %s мараведи." % TotalDay['fixedcost'])

        if TotalDay['HorseFood'] > 0:
            if not TotalDay['HorseStolen']:
                _nextday_lines.append("%s съел сена на %s мараведи." % (player.horse.name, TotalDay['HorseFood']))
            else:
                _nextday_lines.append("%s Пока же он был с вами, он успел сожрать сена на %s мараведи." % (TotalDay['HorseStolen'], TotalDay['HorseFood']))

        _nextday_lines.append("Также %s мешка продуктов съели вы и ваши домочадцы." % DispFrac(TotalDay['fameaten']))

        if TotalDay['dineout'] > 0:
            _nextday_lines.append("Однако вам не хватило запаса продуктов и вы вынужденны были кушать у конкурентов, потратив на это %s мараведи. Люди обратили внимание на то, что вы предпочитаете не есть собственную еду и рассказали об этом своим знакомым." % TotalDay['dineout'])

        if str(player.economy.child_birth_benefit_notice or "").strip():
            _nextday_lines.append(str(player.economy.child_birth_benefit_notice))

        if TotalDay['KidsMoney'] > 0:
            _nextday_lines.append("В воскресенье вам именем герцогини Кончитты Дель Семени было выплаченно %s мараведи воспоможения на детей." % TotalDay['KidsMoney'])

        if TotalWhoreClients.get('georgett', 0) > 0:
            _nextday_lines.append("Развратная %s приняла %s клиентов." % (_geo_name, TotalWhoreClients['georgett']))
        if TotalWhoreClients.get('liza', 0) > 0:
            _nextday_lines.append("Юная %s приняла %s клиентов." % (_liza_name, TotalWhoreClients['liza']))
        if TotalDay['whorerevenue'] > 0:
            _nextday_lines.append("Ваша доля, как договоренно, составила %s мараведи." % TotalDay['whorerevenue'])

        if TotalGloryHoleClients.get('georgett', 0) > 0:
            _nextday_lines.append("Шустрая %s отсосала %s членов через глорихол." % (_geo_name, TotalGloryHoleClients['georgett']))
        if TotalGloryHoleClients.get('liza', 0) > 0:
            _nextday_lines.append("Молодая, да ранняя %s отсосала %s членов через глорихол." % (_liza_name, TotalGloryHoleClients['liza']))
        if TotalDay['gloryholerevenue'] > 0:
            _nextday_lines.append("Ваша прибыль с глорихола, как и было договоренно, составила %s мараведи." % TotalDay['gloryholerevenue'])

        _nextday_lines.append("На кухне остается %s мешков продуктов." % DispFrac(player.tavern_management.productnum))
        _nextday_lines.append("В погребе остается %s бочонков вина." % DispFrac(player.tavern_management.winenum))

        if player.intimacy.ellona_cursed and player.intimacy.ellona_curse_days <= 0:
            player.intimacy.lift_ellona_curse()
            _nextday_lines.append("ВЫ ПОЧУВСТВОВАЛИ КАК ПРОКЛЯТЬЕ ГРАЦИИ УШЛО. ВАША МУЖСКАЯ СИЛА ВОССТАНОВИЛАСЬ.")

        if str(NewDressCame or "").strip():
            _nextday_lines.append(str(NewDressCame))

        if str(TotalEventsSummary or "").strip():
            _nextday_lines.append(_nextday_clean_report_text(TotalEventsSummary))

        _nextday_lines.append(str(tavernlevel) + " Они расскажут об этом друзьям.")

        if TotalDay['loyalty'] > 0:
            _nextday_lines.append("Ваша популярность увеличивается!")
        elif TotalDay['loyalty'] < 0:
            _nextday_lines.append("Ваша популярность уменьшается!")

        if player.economy.tavern_fame >= 10:
            _nextday_lines.append("Ваша популярность выросла настолько, что в ваш трактир стало заходить больше посетителей!")
            player.tavern_management.visitors += player.economy.tavern_fame
            player.economy.tavern_fame = 0
        elif player.economy.tavern_fame <= -10:
            _nextday_lines.append("Ваш трактир обрел настолько дурную славу, что многие бывшие завсегдатаи стали его избегать!")
            player.tavern_management.visitors += player.economy.tavern_fame
            player.economy.tavern_fame = 0

        for _girl in ('sandra', 'melissa', 'amanda'):
            _nextday_lines.extend(describe_skill_increase(_girl))

        next_day_runtime.report_title = "ОТЧЕТ ЗА ДЕНЬ"
        next_day_runtime.report_body = "\n".join([str(_line) for _line in _nextday_lines if str(_line or "").strip()])
        player.economy.child_birth_benefit_notice = ''
    
    # Reset daily variables
    $ Georgett.set_story_value("foundinchurch", 0)
    $ player.intimacy.set_arousal(0)
    $ player.intimacy.came_today = 0
    $ player.set_stat("energy", 100)
    $ calendar_v2.time_advance_blocked = 1
    call TractirCheckAchievements
    call TractirShowPendingAchievements
    $ player.set_stat("notoriety", 0)
    
    # Ensure minimums
    if player.tavern_management.visitors < 0:
        $ player.tavern_management.visitors = 0
    # Check game over conditions through the shared endings registry.
    call TractirCheckEndings
    $ _tractir_game_over_ending = str(_return or "")

    call stat
    hide screen main_ui
    call screen nextday_report_card_overlay
    
    # End game or return
    if player.economy.money == 0 or player.tavern_management.visitors == 0:
        menu:
            "Начать сначала":
                jump Intro
    else:
        $ _nextday_return_label = str(retlocname or "TavernMain")
        if int(calendar_v2.time_slot() or 0) == 0 and _nextday_return_label == "TavernMain":
            $ _nextday_return_label = "TavernMyRoom"
        call checkTriggers("TavernMyRoom", "sleep", 0)
        $ calendar_v2.time_advance_blocked = 0
        if _nextday_return_label == "TavernMyRoom":
            $ _day_start_save_name = "Начало дня — " + calendar_v2.format_date_ru(calendar_v2.day, calendar_v2.period, calendar_v2.cycle, None, False)
            $ renpy.set_return_stack([])
            $ renpy.loadsave.cycle_saves("quick-", config.quicksave_slots)
            $ renpy.save("quick-1", extra_info=_day_start_save_name, include_screenshot=False)
        jump expression _nextday_return_label
    return


default next_day_runtime = NextDayRuntimeState()


screen nextday_report_card_overlay():
    zorder 130

    $ _title = str(next_day_runtime.report_title or "ОТЧЕТ")
    $ _body = str(next_day_runtime.report_body or "Ничего не произошло.")
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _panel_w = int((config.screen_width - 36) * 0.72)
    $ _panel_h = _usable_h - 24
    $ _panel_x = int((config.screen_width - _panel_w) / 2)

    fixed:
        xpos _panel_x
        ypos 12
        xsize _panel_w
        ysize _panel_h

        add im.Scale("images/rpg_message_bg.png", _panel_w, _panel_h)

        viewport:
            xpos 28
            ypos 24
            xsize _panel_w - 56
            ysize _panel_h - 48
            draggable True
            mousewheel True

            vbox:
                spacing 10

                text _title size 30 color "#000000" italic True xalign 0.5
                text _body:
                    size 18
                    color "#000000"
                    italic True
                    substitute False

                textbutton "Назад":
                    id "nextday_report_back_button"
                    text_size 22
                    text_color "#f7f0de"
                    background "#3a2214"
                    hover_background "#5a3420"
                    xpadding 18
                    ypadding 8
                    xalign 0.5
                    action Return()
