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
            "Закончить разговор":
                $ main_ui_end_talk_state()
                return


label HordusMerchandise:
    $ renpy.dynamic("_hordus_item", "_hordus_price")
    vscene "images/market/mistery_merchant.png"
    $ scene_runtime.text = "Хордус откидывает край покрывала. — Выбирай внимательно. Один редкий товар за месяц; остальное пусть пока подождет своего часа."
    while True:
        menu:
            "Старинный диван — [HordusStaticData.catalog['cursed_sofa_001']] мараведи" if threads["claraPaintingsPath"].completed and tavern.renovation_complete('peephole') and tavern.renovation_complete('glory_hole') and int(threads["claraForestSofa"].num or 0) == 6 and not Sofa.installed:
                $ _hordus_item = "cursed_sofa_001"
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
            if _hordus_item == "cursed_sofa_001":
                $ Sofa.installed = True
                $ scene_runtime.text = "Хордус принимает деньги и распоряжается доставить старинный диван в гостевую комнату вашего трактира, к каменной печи. — Если начнет ворчать, не пугайся. Прежний хозяин тоже жаловался… а потом внезапно уехал из города."
            else:
                $ player.add_item(_hordus_item, 1)
                $ scene_runtime.text = "Хорди передает вам сверток и прячет деньги. — На этот месяц сделка состоялась. Пользуйся с умом."
            call stat
