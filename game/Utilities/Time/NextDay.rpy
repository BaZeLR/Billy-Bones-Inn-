    $ sync_player_state_from_store()    hide screen tavern_report_card_overlay    hide screen time_change_card_overlay    hide screen girl_card_overlay
    hide screen player_card_overlay    hide screen time_change_card_overlay    $ sync_player_state_from_store()    hide screen tavern_report_card_overlay    hide screen time_change_card_overlay    hide screen girl_card_overlay
    hide screen player_card_overlay    hide screen time_change_card_overlay    $ sync_player_state_from_store()    hide screen tavern_report_card_overlay    hide screen time_change_card_overlay    hide screen girl_card_overlay
    hide screen player_card_overlay    hide screen time_change_card_overlay# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# NextDay location - converted from legacy script
default NextDayReportTitle = ""
default NextDayReportBody = ""

init python:
    def _nextday_clean_report_text(text):
        return str(text or "").replace("<br>", "\n").strip()

    def nextday_started_after_midnight():
        try:
        except Exception:
            pass

        try:
        except Exception:
            pass

        try:
            try:
            current_hour = int(calendar_v2.hour or 0) % 24
        except Exception:
            try:
                current_hour = int(hour or 0) % 24
            except Exception:
                current_hour = 0

        except Exception:
            try:
                current_hour = int(hour or 0) % 24
            except Exception:
                current_hour = 0

        return 0 <= current_hour < 6

    def nextday_pick_post_sleep_event_label():
        try:
            Sandra.ensure_story_defaults()
        except Exception:
            return ""

        try:
            current_time = int(time or 0)
        except Exception:
            current_time = 0

        if (
            current_time == 0
            and Sandra.weekly_thanks_event_ready()
        ):
            try:
                return str(Sandra.weekly_thanks_target_label() or "")
            except Exception:
                return ""

        return ""

label NextDay(retlocname, timepassed):
    $ visitorshappy = 0
    $ SomebodyCums = 0
    $ _nextday_skip_first_calendar_roll = nextday_started_after_midnight()
    
    python:
        TotalEventsSummary = ''
        ExtraEvents = ''
        iDaysCount = 0
        cookincr = {}
        cleanincr = {}
        waitressincr = {}
        
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
        $ CurDay = {}
        call NextDay_TavernDaily

        call DisplayTavernEventsSummary(day, month, year)
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
        $ player_state(False).daily_maintenance(1)
        
        call NextDay_NewDayEvents
        call CreateTavernEvents
        
        $ iDaysCount += 1
        call stat

    # Calculate revenues
    python:
        TotalDay['whorerevenue'] = TotalWhoreClients['georgett']*3 + TotalWhoreClients['liza']*3
        TotalDay['gloryholerevenue'] = TotalGloryHoleClients['georgett']*2 + TotalGloryHoleClients['liza']*2
        
        player.economy.tavern_fame += TotalDay['loyalty']
        money += (TotalDay['revenue'] - TotalDay['dineout'] - TotalDay['fixedcost'] +
                TotalDay['whorerevenue'] + TotalDay['gloryholerevenue'] +
                TotalDay['KidsMoney'] + (600 if KidBirthPosobie else 0))
        
        NewDressCame = ''
        
        # Handle dress delivery
        if DressProduced:
            if DressBuyer == 'You':
                dress_name = ShortDressName.get(DressProduced, DressProduced).lower()
                NewDressCame = f'Утром прибежал посыльный из лавки Фараго и принес вам ваш заказ - {dress_name}.'
                player.appearance.add_dress(DressProduced, int(dayspassed or 0))
                
            if money >= 50:
                NewDressCame += f' Вы поблагодарили мальчишку, дав ему 5 мараведи, и положили обнову в ларь.'
                money -= 5
            else:
                NewDressCame += f' Вы забрали заказ, проигнорировав протянутую ладошку мальчишки и не дав ему ничего на чай. А обновку вы положили в ларь.'
                Irma.change_social(friend_delta=-1)
                
        DressProduced = ''
        DressBuyer = ''
        
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
        _geo_name = str(RealName.get('georgett', 'Жоржетта') or 'Жоржетта')
        _liza_name = str(RealName.get('liza', 'Лизетта') or 'Лизетта')

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
                _nextday_lines.append("%s съел сена на %s мараведи." % (MyStallion, TotalDay['HorseFood']))
            else:
                _nextday_lines.append("%s Пока же он был с вами, он успел сожрать сена на %s мараведи." % (TotalDay['HorseStolen'], TotalDay['HorseFood']))

        _nextday_lines.append("Также %s мешка продуктов съели вы и ваши домочадцы." % DispFrac(TotalDay['fameaten']))

        if TotalDay['dineout'] > 0:
            _nextday_lines.append("Однако вам не хватило запаса продуктов и вы вынужденны были кушать у конкурентов, потратив на это %s мараведи. Люди обратили внимание на то, что вы предпочитаете не есть собственную еду и рассказали об этом своим знакомым." % TotalDay['dineout'])

        if str(KidBirthPosobie or "").strip():
            _nextday_lines.append(str(KidBirthPosobie))

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

        if CursedByEllona > 0 and CursedByEllonaDays <= 0:
            CursedByEllona = 0
            player.intimacy.can_cum_daily += CursedByEllonaReduce
            CursedByEllonaDays = 0
            CursedByEllonaReduce = 0
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

        NextDayReportTitle = "ОТЧЕТ ЗА ДЕНЬ"
        NextDayReportBody = "\n".join([str(_line) for _line in _nextday_lines if str(_line or "").strip()])
        KidBirthPosobie = ''
    
    # Reset daily variables
    $ Georgett.set_story_value("foundinchurch", 0)
    $ player.intimacy.set_arousal(0, "You")
    $ player.intimacy.came_today = 0
    $ energy = 100
    $ BlockTimeAdvance = 1
    call TractirCheckAchievements
    call TractirShowPendingAchievements
    $ notoriety = 0
    
    # Ensure minimums
    if player.tavern_management.visitors < 0:
        $ player.tavern_management.visitors = 0
    if money < 0:
        $ money = 0
        
    if money < 0:
        $ money = 0
        
    if money < 0:
        $ money = 0
        
    # Check game over conditions through the shared endings registry.
    call TractirCheckEndings
    $ _tractir_game_over_ending = str(_return or "")

    call stat
    hide screen main_ui
    call screen nextday_report_card_overlay
    $ checkpoint_tractir_progress("next_day", True)
    
    # End game or return
    if player.economy.money == 0 or player.tavern_management.visitors == 0:
        menu:
            "Начать сначала":
                jump Intro
    else:
        $ _nextday_return_label = str(retlocname or "TavernMain")
        if int(time or 0) == 0 and _nextday_return_label == "TavernMain":
            $ _nextday_return_label = "TavernMyRoom"
        $ _nextday_post_sleep_label = str(nextday_pick_post_sleep_event_label() or "")
        if _nextday_post_sleep_label != "":
            call expression _nextday_post_sleep_label pass (_nextday_return_label,)
        jump expression _nextday_return_label
    return


screen nextday_report_card_overlay():
    zorder 130

    $ _title = str(NextDayReportTitle or "ОТЧЕТ")
    $ _body = str(NextDayReportBody or "Ничего не произошло.")
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
                text _body size 18 color "#000000" italic True

                textbutton "Назад":
                    text_size 22
                    text_color "#f7f0de"
                    background "#3a2214"
                    hover_background "#5a3420"
                    xpadding 18
                    ypadding 8
                    xalign 0.5
                    action Return()
