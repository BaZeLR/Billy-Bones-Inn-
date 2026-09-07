# ================================================================================
# Clarissa's forest discovery, hidden stash, and cursed-sofa continuation.
# Availability and order are owned only by claraForestSofa in StoryEventRuntime.rpy.
# ================================================================================


label story_clara_forest_follow_0:
    $ main_ui_begin_native_scene_state("Кларисса в лесу")
    show screen main_ui
    vscene "images/clara/forest_clara_encounter.png"
    $ scene_runtime.text = "На лесной поляне вы замечаете Клариссу. Она уверена, что за ней никто не следит, и потому сворачивает с обычной дороги на узкую тропу. После всего услышанного на рынке случайной прогулкой это уже не выглядит."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Тихо проследить за Клариссой":
            pass

        "Заговорить с Клариссой" if int(Clara.rel or 0) >= 5:
            call IntClaraTalk("clara")
            $ main_ui_end_native_scene_state()
            return True

    vscene "images/clara/forest_clara_encounter_2.png"
    $ scene_runtime.text = "Кларисса долго идет через заросли, собирает в мешок травы и несколько раз проверяет след за спиной. У старой водокачки она исчезает между деревьями так уверенно, словно знает скрытую тропу наизусть. Сегодня вы не находите ни тайника, ни сообщников, но теперь знаете: ее лесные прогулки продолжатся."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Отступить, пока она вас не заметила":
            pass

    $ calendar_v2.advance_minutes(30)
    $ player.change_stat("energy", -5)
    call stat
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_forest_horse_prank_1:
    $ main_ui_begin_native_scene_state("Кларисса у озера")
    show screen main_ui
    vscene "images/general/lake_forest view.jpg"
    $ scene_runtime.text = "У озера вы заводите коня в воду, смываете с него дорожную грязь, а затем раздеваетесь и сами окунаетесь с головой. После купания вы еще долго вычесываете мокрую гриву и не замечаете внимательного взгляда из-за деревьев."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закончить купание и чистку коня":
            pass

    vscene "images/clara/forest_clara_0.png"
    $ scene_runtime.text = "Когда вы возвращаетесь к берегу, рубаха, штаны и сапоги исчезли. Из-за поваленного дерева слышится тихий смех Клариссы. Она наблюдала за вашим купанием и решила отплатить вам за прежнюю слежку."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Потребовать вернуть одежду":
            pass

    vscene "images/clara/forest_clara_1.png"
    $ scene_runtime.text = "Кларисса кладет сверток на ветку, но не отворачивается, пока вы выходите из воды. «Теперь мы квиты, Стефан», — объявляет она с совершенно невинным видом. Перед уходом девушка предлагает в следующий раз не прятаться по кустам, а искупаться вместе."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Принять ее вызов":
            pass

    $ calendar_v2.advance_minutes(60)
    $ player.appearance.wash()
    $ player.change_stat("fun", 5)
    $ player.economy.tavern_fame = _player_clamp(player.economy.tavern_fame + 1, -20, 20)
    call stat
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_forest_shared_bath_2:
    $ main_ui_begin_native_scene_state("Купание с Клариссой")
    show screen main_ui
    vscene "images/clara/forest_clara_bath.png"
    $ scene_runtime.text = "Через несколько дней Кларисса действительно приходит к озеру. На этот раз она не убегает и не заставляет вас притворяться, будто вы случайно встретились. Девушка складывает платье на траву и первой входит в воду."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Раздеться и войти следом":
            pass

    vscene "images/clara/forest_clara_bath_2.png"
    $ scene_runtime.text = "Вы купаетесь нагими, держась на расстоянии, которое постепенно становится все меньше. Кларисса смеется над вашей осторожностью и говорит, что в лесу ей хочется выглядеть не примерной дочерью купца, а настоящей разбойницей. Если вам попадется хороший бандитский костюм, она с удовольствием примет такой подарок."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пообещать поискать костюм":
            pass

    vscene "images/clara/forest_clara_bath_3.png"
    $ scene_runtime.text = "На берегу Кларисса нарочно медлит с тонкой мокрой сорочкой, позволяя вам рассмотреть ее почти без прикрытия. Потом быстро одевается, целует вас в щеку и исчезает на скрытой тропе."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Проводить ее взглядом":
            pass

    vscene "images/clara/forest_clara_bath_4.png"
    $ scene_runtime.text = "Последним вам запоминается ее лукавый взгляд через плечо: Кларисса явно довольна тем, что заставила вас забыть об осторожности. Уходя к скрытой тропе, она не оставляет на берегу ничего из своих вещей."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к своим делам":
            pass

    $ Clara.change_social(friend_delta=1, open_delta=1)
    $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
    $ calendar_v2.advance_minutes(60)
    $ player.appearance.wash()
    $ player.change_stat("fun", 10)
    call stat
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_grocery_dirt_3:
    $ main_ui_begin_native_scene_state("Лесная грязь")
    show screen main_ui
    vscene "images/clara/market_day.png"
    $ scene_runtime.text = "В продуктовой лавке вы неожиданно сталкиваетесь с Клариссой. На подоле ее платья и на носках туфель засохла темная лесная грязь, а из сумки выглядывает та самая грубая веревка, которую вы видели у старой водокачки."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Спросить, откуда на туфлях лесная грязь":
            pass

    $ scene_runtime.text = "Кларисса слишком быстро отвечает, что просто ходила за травами. Затем замечает ваш взгляд на сумке, путается в объяснениях, задевает корзину с яблоками и принимается собирать их с таким усердием, будто от этого зависит ее жизнь. В конце концов она шепчет: «Не здесь. Если уже нашел мои панталоны, пусть твой пес возьмет след у старой водокачки. Потом поговорим обо всем»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Не устраивать сцену в лавке":
            pass

    $ calendar_v2.advance_minutes(15)
    call stat
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_forest_sofa_stash_4:
    $ main_ui_begin_native_scene_state("Тайник Клариссы")
    show screen main_ui
    vscene "images/forest/hidden_path.png"
    $ scene_runtime.text = "У старой водокачки вы даете псу обнюхать панталоны Клариссы. %s сразу берет след, ведет вас по едва заметной тропе и останавливается у дерева с вырезанным знаком. Походная лопата вскоре ударяется о завернутый в промасленную ткань сверток. Внутри лежат шестьсот мараведи и записи о продаже краденых лошадей." % str(dog.pet_name or "Пес")
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Запомнить место и поговорить с Клариссой":
            pass

    $ player.change_stat("energy", -10)
    $ calendar_v2.advance_minutes(60)
    call stat
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_clara_forest_confession_5:
    $ renpy.dynamic("_clara_horse_refund", "_clara_stash_take")
    $ main_ui_begin_native_scene_state("Правда Клариссы")
    show screen main_ui
    vscene "images/clara/wineSellar_clara_talk_6.png"
    $ _clara_horse_refund = max(0, int(player.horse.stolen_purchase_price or 0) // 2)
    $ _clara_stash_take = 600 + _clara_horse_refund
    $ scene_runtime.text = "Когда вы называете старую водокачку, собаку и закопанный сверток, Кларисса перестает притворяться. Она запирает дверь погребка и просит дать ей договорить до конца."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Выслушать всю правду":
            pass

    vscene "images/clara/forest_clara_bath_3.png"
    $ scene_runtime.text = "Отец Альбер с детства учил ее считать деньги, торговаться и держаться как настоящая госпожа, а теперь собирается выдать за столичного жениха ради выгодной связи. Спасаясь от этой сделки, Кларисса тайком уходила к разбойничьему лагерю и мечтала купить себе место среди людей, которые не спрашивают разрешения у семьи.\n\nИменно Кларисса придумала кражу лошадей, нашла покупателя и направляла Монгола. Через непристойные рисунки, сплетни и визиты в трактир она также пыталась сделать Аманду и Мелиссу сговорчивее для замыслов Легаре. Ради собственной свободы она стала использовать чужое доверие тем же способом, каким Легаре использовал ее."
    if _clara_horse_refund > 0:
        $ scene_runtime.text += "\n\nСреди записей есть и ваша украденная лошадь. Кларисса признает долг и отделяет половину уплаченной вами цены — %d мараведи. Эти деньги она готова вернуть независимо от того, что вы решите с остальным тайником." % _clara_horse_refund
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Спросить о Легаре и настоящем отце":
            pass

    $ scene_runtime.text = "Кларисса подтверждает то, что уже открыла вам в разговоре о рисунках: Легаре не ее родной отец. Элоиза родила ее до брака, а имя настоящего отца осталось неизвестным. Легаре воспитал Клариссу, но превратил зависимость приемной дочери в право распоряжаться ее телом, браком и тайнами.\n\nТеперь Кларисса просит защиты. Если вы не выдадите ее семье и страже, она прекратит помогать планам Легаре, расскажет все о женихе и разбойничьем лагере, вернет доверие девушек и будет использовать свое воспитание на пользу трактиру."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Простить Клариссу, вернуть тайник и панталоны":
            if _clara_horse_refund > 0:
                $ player.add_money(_clara_horse_refund)
            $ player.horse.stolen_purchase_price = 0
            if int(player.item_count("clara_pantaloons_001") or 0) > 0:
                $ player.remove_item("clara_pantaloons_001", 1)
            $ Clara.drawings_secret_known = True
            $ Clara.merchant_contact_unlocked = True
            $ Clara.change_social(friend_delta=4, open_delta=2)
            $ Clara.trust = min(20, int(Clara.trust or 0) + 4)
            if threads["claraTavernVisit"].completed:
                $ threads["claraTavernVisit"].advanceTo(6, force_active=True)
            $ event_runtime.active_thread.advance()
            $ main_ui_end_native_scene_state()
            return True

        "Простить Клариссу, но оставить деньги и улику":
            $ player.add_money(_clara_stash_take)
            $ player.horse.stolen_purchase_price = 0
            $ Clara.drawings_secret_known = True
            $ Clara.merchant_contact_unlocked = True
            $ Clara.change_social(friend_delta=2, open_delta=2)
            $ Clara.trust = min(20, int(Clara.trust or 0) + 2)
            if threads["claraTavernVisit"].completed:
                $ threads["claraTavernVisit"].advanceTo(6, force_active=True)
            $ event_runtime.active_thread.advance()
            $ main_ui_end_native_scene_state()
            return True

        "Отказать в защите и передать доказательства страже":
            $ player.add_money(_clara_stash_take)
            $ player.horse.stolen_purchase_price = 0
            $ Clara.change_social(friend_delta=-5)
            $ Clara.trust = max(0, int(Clara.trust or 0) - 5)
            $ event_runtime.active_thread.abort()
            $ main_ui_end_native_scene_state()
            return True
