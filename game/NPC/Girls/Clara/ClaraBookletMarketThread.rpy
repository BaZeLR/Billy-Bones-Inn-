# ================================================================================
# Clara booklet market authored event labels.
#
# Event availability is owned by claraBookletMarket in StoryEventRuntime.rpy.
# This file owns only the played scene: vscene, text, menu choices, consequences,
# time cost, and direct thread progression.
# ================================================================================


# Event: first daytime Clara booklet sighting at MarketPlace.
# Choice flow:
# - follow: exploration < 80 fails, keeps thread on this stage, records retry cooldown
# - follow: exploration >= 80 succeeds, reveals booklet merchant, optionally confronts Clara, advances thread
# - ignore: keeps thread on this stage and records retry cooldown
label story_clara_market_booklet_0:
    $ SignalBlockTime = 1
    $ UI_mode = "event"

    vscene "images/clara/market_day.png"
    if int(Clara.var.get("market_intro_seen", 0) or 0) == 1:
        $ MainTxt = "Днем на рынке снова мелькает фигура в легком плаще. Вы узнаете Клариссу раньше, чем она успевает скрыть лицо. Девушка замечает вас, поспешно натягивает капюшон и идет быстрее, будто совершенно не хочет, чтобы ее здесь окликали.\n\nЕсли уж вы хотите узнать, чем она занимается, сейчас самое время попробовать проследить за ней."
    else:
        $ MainTxt = "На дневном рынке среди покупателей вы замечаете фигуру в плаще. Сначала это просто случайный силуэт в толпе, но затем вы узнаете Клариссу, дочку своего винного поставщика.\n\nВы уже собираетесь окликнуть ее, но Кларисса, едва встретившись с вами взглядом, поспешно набрасывает на голову капюшон и сразу идет быстрее между рядами лавок. Похоже, у нее здесь какие-то совсем частные дела, и узнавать себя она сейчас не хочет."
        $ Clara.var["market_intro_seen"] = 1
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Проследить за Клариссой":
            jump story_clara_market_booklet_follow

        "Не вмешиваться":
            jump story_clara_market_booklet_ignore


label story_clara_market_booklet_ignore:
    vscene "images/clara/market_day.png"
    $ MainTxt = "Вы решаете не вмешиваться и позволяете Клариссе скрыться среди торговых рядов."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    $ Clara.var["market_follow_failed_day"] = int(dayspassed or 0)
    $ Clara.var["market_follow_failed_hour"] = int(hour or 0)
    $ LastAdvancedMinutes = 15
    $ calendar_v2.advance_minutes(15)
    $ npc_schedule_sync_all()
    $ werecat_sync_profile()
    $ player_state().change_stat("energy", -2)
    call stat
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


label story_clara_market_booklet_follow:
    if int(exploration or 0) < 80:
        vscene "images/clara/market_day.png"
        $ MainTxt = "Вы стараетесь не отстать, но дневной рынок слишком шумный и тесный. Стоит вам замешкаться на пару шагов, как Кларисса ускользает между рядами и будто растворяется среди чужих спин.\n\nПохоже, без лучшей сноровки в слежке вы просто потеряете ее снова."
        $ CurLocDesc = MainTxt
        "[MainTxt]"

        $ Clara.var["market_follow_failed_day"] = int(dayspassed or 0)
        $ Clara.var["market_follow_failed_hour"] = int(hour or 0)
        $ LastAdvancedMinutes = 30
        $ calendar_v2.advance_minutes(30)
        $ npc_schedule_sync_all()
        $ werecat_sync_profile()
        $ player_state().change_stat("energy", -5)
        call stat
        $ UI_mode = "scene"
        $ SignalBlockTime = 0
        return True

    vscene "images/clara/market_bookletDeal.png"
    $ MainTxt = "На этот раз вы не теряете Клариссу в толпе. Держась в стороне, вы видите, как она сворачивает к неприметному торговцу, которого почти не видно с центральных рядов. Обмен короткий и явно привычный: Кларисса по одной передает ему тонкие книжечки, похожие на небольшие буклеты, а тот быстро сует их в сумку и так же быстро отсчитывает ей деньги.\n\nТеперь уже ясно, что речь идет не о простой прогулке по рынку. Кларисса что-то сбывает через этого таинственного торговца."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Подойти к Клариссе и торговцу" if int(Melissa.var.get("drawings_found", 0) or 0) == 1 or int(Clara.var.get("drawings_secret_known", 0) or 0) == 1:
            jump story_clara_market_booklet_confront

        "Тихо уйти":
            jump story_clara_market_booklet_follow_success_leave


label story_clara_market_booklet_follow_success_leave:
    $ Clara.var["booklet_market_seen"] = 1
    $ LastAdvancedMinutes = 30
    $ calendar_v2.advance_minutes(30)
    $ npc_schedule_sync_all()
    $ werecat_sync_profile()
    $ player_state().change_stat("energy", -5)
    call stat
    $ thread.advance()
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


label story_clara_market_booklet_confront:
    vscene "images/clara/market_bookletDeal.png"

    $ _clara_market_bonus = 1
    if str(player_state().appearance.current_dress or "") == "thiefdress":
        $ _clara_market_bonus += 1
    if int(Clara.rel or 0) >= 7:
        $ _clara_market_bonus += 1

    if str(player_state().appearance.current_dress or "") == "thiefdress" and int(Clara.rel or 0) >= 7:
        $ MainTxt = "Вы выходите из-за лотка без лишней суеты и даете Клариссе понять, что уже видели похожие непристойные рисунки у Мелиссы. На секунду она белеет, но, заметив ваш бандитский костюм и поняв, что вы не собираетесь устраивать сцену, быстро берет себя в руки.\n\nКларисса коротко просит не устраивать разговор прямо здесь, а таинственный торговец запоминает вас уже без прежней враждебности. Похоже, с этого дня он готов показывать вам свой особый товар не чаще раза в месяц, а сама Кларисса становится с вами заметно откровеннее."
    else:
        $ MainTxt = "Вы подходите ближе и спокойно даете понять Клариссе, что уже видели похожие непристойные рисунки и догадываетесь, чем она тут занимается. Девушка сразу напрягается, но, услышав, что вы не собираетесь ее выдавать, все же выдыхает.\n\nБез долгих разговоров Кларисса просит не поднимать шум на рынке. Торговец рядом молча запоминает вас взглядом. Похоже, теперь и он будет считать вас своим человеком, а сама Кларисса станет откровеннее лишь если решит, что вам действительно можно доверять."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    $ Clara.var["drawings_secret_known"] = 1
    $ Clara.var["merchant_contact_unlocked"] = 1
    $ Clara.openness = min(20, int(Clara.openness or 0) + _clara_market_bonus)
    $ Clara.trust = min(20, int(Clara.trust or 0) + max(1, _clara_market_bonus - 1))
    $ Clara.var["trust"] = int(Clara.trust or 0)
    jump story_clara_market_booklet_follow_success_leave


# Event: evening Clara market sighting.
# Choice flow:
# - follow: exploration < 100 fails, keeps thread on this stage, records retry cooldown
# - follow: exploration >= 100 succeeds, advances to the Mongol deal scene
# - leave: keeps thread on this stage
label story_clara_market_booklet_2:
    $ SignalBlockTime = 1
    $ UI_mode = "event"

    vscene "images/clara/market_night.png"
    $ MainTxt = "Вечером рынок закрыт, и площадь выглядит почти пустой. У закрытых лавок задержались лишь несколько человек, поэтому фигура в плаще сразу бросается в глаза. Когда она проходит ближе к фонарю, вы узнаете Клариссу.\n\nСтоит ей заметить ваш взгляд, как девушка глубже натягивает капюшон и быстро уходит в сторону закутка у конного торга. Хм. Очень интересно, что она делает здесь в такое время.\n\nПохоже, на этот раз дело идет уже не о книжечках, а о чем-то более грязном."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Тихо проследить за Клариссой":
            jump story_clara_market_booklet_2_follow

        "Не рисковать":
            jump story_clara_market_booklet_2_ignore


label story_clara_market_booklet_2_ignore:
    vscene "images/clara/market_night.png"
    $ MainTxt = "Вы не рискуете ходить за Клариссой по закрытому рынку. Если здесь и происходит что-то грязное, сегодня вы предпочитаете не лезть в темный закуток без подготовки."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    $ LastAdvancedMinutes = 15
    $ calendar_v2.advance_minutes(15)
    $ npc_schedule_sync_all()
    $ werecat_sync_profile()
    $ player_state().change_stat("energy", -2)
    call stat
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


label story_clara_market_booklet_2_follow:
    $ Clara.var["market_evening_intro_seen"] = 1

    if int(exploration or 0) < 100:
        vscene "images/clara/market_night.png"
        $ MainTxt = "Закрытый вечерний рынок куда опаснее для слежки, чем дневная толпа. Стоит вам задеть чью-то корзину и чуть замешкаться, как Кларисса вместе с Монголом растворяются в темном закутке между пустеющими рядами. Без лучшей сноровки здесь их не удержать."
        $ CurLocDesc = MainTxt
        "[MainTxt]"

        $ Clara.var["market_follow_failed_day"] = int(dayspassed or 0)
        $ Clara.var["market_follow_failed_hour"] = int(hour or 0)
        $ LastAdvancedMinutes = 30
        $ calendar_v2.advance_minutes(30)
        $ npc_schedule_sync_all()
        $ werecat_sync_profile()
        $ player_state().change_stat("energy", -5)
        call stat
        $ UI_mode = "scene"
        $ SignalBlockTime = 0
        return True

    $ LastAdvancedMinutes = 30
    $ calendar_v2.advance_minutes(30)
    $ npc_schedule_sync_all()
    $ werecat_sync_profile()
    $ player_state().change_stat("energy", -5)
    call stat
    $ thread.advance()
    jump story_clara_market_booklet_3


# Event: Clara and Mongol horse-theft deal.
# Consequence: the deal is seen and the thread advances.
label story_clara_market_booklet_3:
    $ SignalBlockTime = 1
    $ UI_mode = "event"

    vscene "images/clara/mongolTalk.png"
    $ MainTxt = "На этот раз вы держитесь достаточно далеко и не выдаете себя ни шагом, ни тенью. Кларисса уводит вас к самому краю рынка, где ее уже ждет Монгол. Разговор идет быстро и вполголоса, но вы успеваете разобрать главное.\n\nКларисса велит ему взять не первую попавшуюся клячу, а хорошую лошадь, чтобы потом продать ее с наваром. Деньги она требует делить честно, потому что именно она нашла покупателя и подсказала, где можно взять товар так, чтобы шум поднялся не сразу. Монгол в ответ ухмыляется, обещает свою долю и, будто нарочно, поддевает ее, что в ее любимом бандитском костюме она выглядела бы среди его людей вовсе как своя.\n\nТеперь уже ясно, что Кларисса не просто прячет от вас книжечки. Она сознательно полезла в настоящую грязь."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Запомнить услышанное и уйти":
            pass

    $ Clara.var["mongol_theft_seen"] = 1
    $ Clara.openness = min(20, int(Clara.openness or 0) + 1)
    $ thread.advance()
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


# Event: Clara confesses her reason in WineStore talk.
# Consequence: confession is marked, openness/friendship change, and the thread advances.
label story_clara_market_booklet_4:
    $ SignalBlockTime = 1
    $ UI_mode = "event"

    vscene "images/clara/mongolTalk.png"
    $ MainTxt = "Вы дожидаетесь удобного момента и без окриков говорите Клариссе, что видели ее вечерний разговор с Монголом. Девушка сначала белеет, потом зло сжимает губы, но быстро понимает, что вы пришли не сдавать ее отцу.\n\n\"Да, это я его подбила,\" признается она наконец. \"Мне нужны деньги. Отец уже подбирает мне старого хрыча в столице, и весь этот брак будет не для меня, а для его торговли. Я не собираюсь ехать туда смирной куклой.\" Она нервно усмехается и добавляет, что книжечки, рисунки и все разговоры про свободу для нее давно перестали быть просто романтической чушью. \"Хочется хоть раз жить не по чужому счету. А Монгол обещал, что если я соберу достаточно денег, то в его тайном кругу мне найдут место. Хоть кем. Хоть рисовальщицей, хоть этой их девкой для сценок. Знаю, звучит грязно. Но это все равно лучше, чем лечь под старого вонючего дурака по приказу отца.\"\n\nСказав это, Кларисса смотрит на вас уже не как на случайного покупателя, а как на человека, который теперь знает слишком много."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Оставить услышанное между вами":
            pass

    $ _clara_escape_bonus = 1
    if str(player_state().appearance.current_dress or "") == "thiefdress":
        $ _clara_escape_bonus += 1
    if int(Clara.rel or 0) >= 7:
        $ _clara_escape_bonus += 1
    $ Clara.var["escape_confessed"] = 1
    $ Clara.var["drawings_secret_known"] = 1
    $ Clara.openness = min(20, int(Clara.openness or 0) + _clara_escape_bonus)
    $ Clara.trust = min(20, int(Clara.trust or 0) + max(1, _clara_escape_bonus - 1))
    $ Clara.var["trust"] = int(Clara.trust or 0)
    $ LastAdvancedMinutes = 30
    $ calendar_v2.advance_minutes(30)
    $ npc_schedule_sync_all()
    $ werecat_sync_profile()
    call stat
    $ thread.advance()
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


# Event: HunterClub rumor reveals Mongol's arrest.
# Consequence: the stocks arrest day is recorded and the thread advances.
label story_clara_market_booklet_5:
    $ SignalBlockTime = 1
    $ UI_mode = "event"

    vscene "images/general/hunter_store_catInfo.png"
    $ MainTxt = "Едва вы входите в охотничий клуб, как из угла до вас доносится горячий пересказ свежей городской новости. Охотники с явным удовольствием обсуждают, как стража наконец-то сцапала конокрада, слишком уж долго крутившегося вокруг рынка и конного торга.\n\n\"Сидит теперь у караулки в колодках, вместе с парой таких же голодранцев,\" хмыкает один. \"Пусть народ посмотрит, может поумнеют.\" Другой замечает, что десятник Циммерман теперь ходит важный, как будто сам лично всю шайку выволок за шкирку.\n\nСудя по обрывкам слов, речь идет о Монголе."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Запомнить слух":
            pass

    $ Mongol.var["StocksArrestDay"] = int(dayspassed or 0)
    $ LastAdvancedMinutes = 15
    $ calendar_v2.advance_minutes(15)
    $ npc_schedule_sync_all()
    $ werecat_sync_profile()
    call stat
    $ thread.advance()
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


# Event: the player sees Mongol in the stocks.
# Consequence: stocks seen flag is recorded and the thread advances.
label story_clara_market_booklet_6:
    $ SignalBlockTime = 1
    $ UI_mode = "event"

    vscene "images/mongolStock.png"
    $ MainTxt = "На рыночной площади, возле караулки, стоят тяжелые колодки. В них вместе с еще парой помятых головорезов сидит и Монгол. От прежней ярмарочной ухмылки в нем мало что осталось: губа разбита, рубаха грязная, но глаза все еще бегают живо.\n\nЗаметив вас, он дергается и шипит сквозь зубы: \"Стефан, брат, не губи. Я тут с голоду загнусь раньше, чем меня судить начнут. Принеси ночью пожрать, а там, может, и поговорим. Я добро помню. И про Клариссу тоже помню.\""
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Запомнить его просьбу":
            pass

    $ Mongol.var["StocksSeen"] = 1
    $ thread.advance()
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


# Event: feed Mongol at the stocks.
# Choice flow:
# - give food: consumes food, records the day, advances thread
# - leave: keeps thread on this stage
label story_clara_market_booklet_7:
    $ SignalBlockTime = 1
    $ UI_mode = "event"

    vscene "images/mongolStock.png"
    $ MainTxt = "Ночью у караулки тихо, только где-то внутри переговариваются сонные стражи. Монгол в колодках шевелится и, увидев вас, сразу подается вперед.\n\n\"Ну что, принес чего-нибудь?\" шепчет он. \"Я тут второй день на одной воде. Помоги сейчас, и я потом не забуду.\""
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Передать Монголу еду из трактира" if int(productnum or 0) > 0:
            jump story_clara_market_booklet_feed_mongol

        "Уйти и вернуться позже":
            $ UI_mode = "scene"
            $ SignalBlockTime = 0
            return True


label story_clara_market_booklet_feed_mongol:
    vscene "images/mongolStock.png"
    $ MainTxt = "Вы незаметно протягиваете Монголу завернутую в тряпицу еду из трактирной кухни. Тот жадно хватается за нее обеими руками, давится первыми кусками и тут же начинает шептать благодарности.\n\n\"Вот это по-людски, Стефан. Еще бы отмычки добыть, да стражу чем-нибудь отвлечь... Тогда я не просто вылезу, а еще и твой долг запомню. Если потом занесет к людям Робина, скажу им, кто ты такой.\""
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    $ productnum = max(0, int(productnum or 0) - 1)
    $ Mongol.var["StocksFoodDay"] = int(dayspassed or 0)
    $ LastAdvancedMinutes = 15
    $ calendar_v2.advance_minutes(15)
    $ npc_schedule_sync_all()
    $ werecat_sync_profile()
    call stat
    $ thread.advance()
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


# Event: order lockpicks from Draupnir.
# Choice flow:
# - pay: consumes money, records lockpick order, advances thread
# - leave: keeps thread on this stage
label story_clara_market_booklet_8:
    $ SignalBlockTime = 1
    $ UI_mode = "event"

    vscene "images/draupnir/dwarf1.jpg"
    $ MainTxt = "Вы находите Драупнира за верстаком и, не мудрствуя лукаво, объясняете, что вам нужны очень тонкие отмычки. Гном сперва косится на вас с подозрением, потом только фыркает.\n\n\"Ничего не знаю и знать не хочу, для какой двери тебе такая железяка,\" ворчит он. \"Но если работа тонкая и молчаливая, то это ко мне. За сорок мараведи сделаю хороший набор, который и в сапог спрятать не стыдно.\""
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Заплатить 40 мараведи за тонкие отмычки" if int(money or 0) >= 40:
            jump story_clara_market_booklet_lockpicks_order

        "Не заказывать пока":
            $ UI_mode = "scene"
            $ SignalBlockTime = 0
            return True


label story_clara_market_booklet_lockpicks_order:
    vscene "images/draupnir/dwarf1.jpg"
    $ MainTxt = "Драупнир быстро прячет деньги, вытаскивает из ящика тонкий кожаный сверток и сует его вам почти не глядя.\n\n\"Вот. Только если с этим полезешь куда не надо, не вздумай потом ссылаться на меня,\" бурчит гном. Судя по тяжести свертка, набор отмычек у вас теперь есть."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    $ money = int(money or 0) - 40
    $ DraupnirVar["MongolLockpickOrderDay"] = int(dayspassed or 0)
    $ LastAdvancedMinutes = 15
    $ calendar_v2.advance_minutes(15)
    $ npc_schedule_sync_all()
    $ werecat_sync_profile()
    call stat
    $ thread.advance()
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True


# Event: release Mongol from the stocks.
# Choice flow:
# - release: consumes food/wine, updates consequences, completes the thread
# - leave: keeps thread on this stage
label story_clara_market_booklet_9:
    $ SignalBlockTime = 1
    $ UI_mode = "event"

    vscene "images/mongolStock.png"
    $ MainTxt = "Следующей ночью вы возвращаетесь к караулке уже подготовленным. Монгол сразу понимает это по вашему лицу и только сильнее вжимается в колодки, чтобы не привлекать лишних взглядов.\n\nТеперь все упирается в одно: если вы хотите вытащить его отсюда, надо сперва умаслить стражу и отвлечь ее чем-то приятнее ночного дежурства."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    menu:
        "Послать стражникам вино и угощение, а затем освободить Монгола" if int(productnum or 0) > 0 and int(winenum or 0) > 0:
            jump story_clara_market_booklet_release_mongol

        "Передумать и уйти":
            $ UI_mode = "scene"
            $ SignalBlockTime = 0
            return True


label story_clara_market_booklet_release_mongol:
    vscene "images/mongolStock.png"
    $ MainTxt = "Вы заранее посылаете к караулке кувшин вина и хороший ужин из трактира с вежливой припиской: мол, \"Дикий Жеребец\" благодарит городскую стражу за поимку конокрадов. Стража мгновенно добреет к такой заботе. Сам десятник Циммерман замечает, что вот это уже разговор с уважаемым трактирщиком, который умеет ценить порядок в городе.\n\nКогда угощение делает свое дело и дежурные окончательно расслабляются, вы выбираете момент, приседаете к колодкам и пускаете в ход заказанные у Драупнира отмычки. Замок поддается не сразу, но все же тихо щелкает. Монгол выскальзывает из дерева, как уж, шепотом сыплет вам благодарностями и обещает, что люди Робина в Шервуде узнают, кому он обязан свободой.\n\nЕще до рассвета его и след простыл."
    $ CurLocDesc = MainTxt
    "[MainTxt]"

    $ productnum = max(0, int(productnum or 0) - 1)
    $ winenum = max(0, int(winenum or 0) - 1)
    $ tavernfame = int(tavernfame or 0) + 2
    $ Zimmer.change_social(friend_delta=1)
    $ Mongol.var["GuardGiftSent"] = 1
    $ Mongol.var["GuardCaptainKnown"] = 1
    $ Mongol.var["StocksReleased"] = 1
    $ Robin.var["MongolSafePass"] = 1
    $ Robin.var["BlackwoodRoadOpen"] = 1
    $ LastAdvancedMinutes = 30
    $ calendar_v2.advance_minutes(30)
    $ npc_schedule_sync_all()
    $ werecat_sync_profile()
    call stat
    $ thread.complete()
    $ UI_mode = "scene"
    $ SignalBlockTime = 0
    return True
