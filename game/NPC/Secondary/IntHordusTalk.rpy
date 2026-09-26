label story_clara_hordus_market:
    $ main_ui_begin_native_scene_state("Кларисса и таинственный торговец")
    show screen main_ui
    vscene "images/clara/market_bookletDeal.png"
    $ Hordus.last_meeting_day = int(calendar_v2.daysInGame)

    if not Hordus.known:
        "Вы снова замечаете Клариссу возле знакомого торговца. Девушка передает ему сверток с рисунками, а он, не разворачивая бумаги на виду у прохожих, убирает покупку в дорожную сумку. На этот раз Кларисса не пытается скрыться от вас."
        menu:
            "Подойти":
                pass
        "— Это Хордус Папирус, из столицы, — представляет его Кларисса. — Для друзей — Хорди. У него бывают вещи, которых в обычных лавках не найдешь."
        menu:
            "Познакомиться с торговцем":
                pass
        vscene "images/market/mistery_merchant.png"
        $ Hordus.mark_known()
        "— Рад знакомству, хозяин трактира. Кларисса умеет выбирать собеседников, — негромко говорит Хордус. — Я приезжаю дважды в месяц, днем. Даты меняются: дорога любит вносить поправки. Редкости показываю своим, но уступить могу лишь одну за месяц. Иные вещи не любят спешки… да и лишних вопросов."
    else:
        "Кларисса снова продает Хорди свои рисунки. Торговец придирчиво проверяет сверток, отсчитывает деньги и прячет бумаги от чужих глаз. Заметив вас, оба приветственно кивают. Похоже, их торговля продолжается своим чередом."

    menu:
        "Спросить о мебели для гостевой" if story_event_available("talk_hordus", "guest_room_furniture"):
            $ main_ui_end_native_scene_state()
            call checkTriggers("talk_hordus", "guest_room_furniture", 0)
            return True
        "Посмотреть товары Хордуса":
            call HordusMerchandise
        "Вернуться к своим делам":
            pass
    $ main_ui_end_native_scene_state()
    return True


label IntHordusTalk:
    $ main_ui_begin_talk_state("Разговор с " + Hordus.display_name(), "hordus")
    vscene "images/market/mistery_merchant.png"
    if Hordus.known:
        $ scene_runtime.text = "Хорди встречает вас едва заметной улыбкой. На прилавке лежат аккуратно завернутые вещи; ни на одном свертке нет вывески."
    else:
        $ scene_runtime.text = "Незнакомый торговец прикрывает дорожную сумку ладонью. — Здесь не всякий товар для всякого покупателя. Может быть, нас еще представят друг другу."
    while True:
        menu:
            "Спросить о столице" if Hordus.known:
                $ scene_runtime.text = "— В столице охотно платят за то, о чем здесь предпочитают молчать, — отвечает Хорди. — Я лишь помогаю вещам найти своих хозяев. Иногда и хозяевам — свои вещи."
            "Посмотреть товары" if Hordus.known:
                call HordusMerchandise
            "Спросить о мебели для гостевой" if story_event_available("talk_hordus", "guest_room_furniture"):
                call checkTriggers("talk_hordus", "guest_room_furniture", 0)
            "Закончить разговор":
                $ main_ui_end_talk_state()
                return


label HordusMerchandise:
    $ renpy.dynamic("_hordus_item", "_hordus_price")
    vscene "images/market/mistery_merchant.png"
    $ scene_runtime.text = "Хордус откидывает край покрывала. — Выбирай внимательно. Один редкий товар за месяц; остальное пусть пока подождет своего часа."
    while True:
        menu:
            "Роскошное мыло — [HordusStaticData.catalog['luxury_soap_001']] мараведи":
                $ _hordus_item = "luxury_soap_001"
            "Пряная настойка — [HordusStaticData.catalog['libido_tincture_001']] мараведи":
                $ _hordus_item = "libido_tincture_001"
            "Особый гриб — [HordusStaticData.catalog['special_mushroom_001']] мараведи":
                $ _hordus_item = "special_mushroom_001"
            "Назад":
                return

        $ _hordus_price = HordusStaticData.catalog[_hordus_item]
        if not Hordus.known:
            $ scene_runtime.text = "Торговец придерживает сверток: — Сначала нас должны представить друг другу."
        elif Hordus.last_trade_month == int(calendar_v2.cycle) * 100 + int(calendar_v2.period):
            $ scene_runtime.text = "— В этом месяце ты уже сделал выбор. За следующей редкостью приходи в новом месяце, — напоминает Хорди."
        elif player.economy.money < _hordus_price:
            $ scene_runtime.text = "На этот товар у вас сейчас не хватает денег."
        else:
            $ player.spend_money(_hordus_price)
            $ Hordus.last_trade_month = int(calendar_v2.cycle) * 100 + int(calendar_v2.period)
            $ player.add_item(_hordus_item, 1)
            $ scene_runtime.text = "Хорди передает вам сверток и прячет деньги. — На этот месяц сделка состоялась. Пользуйся с умом."
            call stat


label story_hordus_nostar_sofa_lead_0:
    $ main_ui_begin_native_scene_state("Мебель для гостевой")
    show screen main_ui
    vscene "images/market/mistery_merchant.png"
    $ scene_runtime.text = "Когда остальные покупатели отходят от повозки, вы задерживаете Хорди вопросом: — Для гостевой комнаты ничего не найдётся? Хочется чего-нибудь лучше обычной лавки.\n\nТорговец прикрывает товары краем покрывала. — Месяцем раньше я бы показал тебе диван, какого здесь не видывали. Но леди Ностар Линк увидела его первой и заплатила, не торгуясь. Потом прислала записку: диван, мол, слишком много слышит. Забавно. При мне он держал язык за зубами."
    menu:
        "Спросить, где искать леди":
            pass
    $ scene_runtime.text = "— Где мне найти эту леди?\n\nХорди оглядывает рынок и лишь тогда наклоняется ближе. — За кварталом ремесленников, на улице пяти цветных домов. У её дверей привратник смотрит на прохожих так, будто сам пожаловал им дворянство. Моего имени не называй: леди терпеть не может, когда ей навязывают покупателей. Скажи, что ищешь мебель для гостевой. Остальное она расскажет сама — если сочтёт тебя достаточно занятным."
    menu:
        "Поблагодарить Хорди":
            pass
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
