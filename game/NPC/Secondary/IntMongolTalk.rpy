label MongolTalk:
    $ renpy.dynamic("_mongol_talk_new")
    $ _mongol_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != "mongol"
    $ main_ui_begin_talk_state("Разговор с Монголом", "mongol")
    if _mongol_talk_new:
        $ scene_runtime.text = "Монгол выжидающе смотрит на вас, придерживая жеребца за повод."
        $ scene_runtime.location_text = scene_runtime.text

    while True:
        menu:
            "Осмотреть":
                $ scene_runtime.text = "Монгол - торговец лошадьми. Он одет в красную рубаху, широкие штаны и высокие сапоги. В ухе у него серьга а на голове цветная косынка. Он держит за повод оседланного жеребца."
                $ scene_runtime.location_text = scene_runtime.text
                call ShowImageSeq("mongol", "", "portrait", 3)

            "А ты цыган?" if not Mongol.asked_about_gypsy:
                $ scene_runtime.text = "\"Я? Цыган?\" удивился вашему вопросу Монгол. \"Да какой же я цыган, что во мне цыганского? Да я этих цыган просто ненавижу! Я их, если хочешь знать, просто терпеть не могу! Ворье и жулье они! А я честный лошадиный барышник. Даже слишком честный, не поверишь, себе в убыток торгую!\"\n\nВ последнем своем предположении Монгол был прав, вы почему-то ему не поверили."
                $ scene_runtime.location_text = scene_runtime.text
                $ Mongol.asked_about_gypsy = True

            "А чего дороже-то продаешь, раньше же 1000 было?" if Mongol.zimmer_knows_horse_theft and not Mongol.asked_price_increase:
                $ scene_runtime.text = "\"Да я бы и рад подешевле, но ты войди в мое положение! Мне семью кормить надо, а тут еще стража денег с нас, якобы за защиту, требует. Десятник этот картавый целый стольник потребовал, иначе, мол, говорит, нельзя тебе здесь лошадьми торговать. Мол поступлю тогда с тобой по всей строгости закона. А ведь сам знаешь, что за конокра.., в смысле за тороговлю лошадьми без лицензии полагается.\""
                $ scene_runtime.location_text = scene_runtime.text
                $ Mongol.asked_price_increase = True

            "Пару сотен скинешь?" if not Mongol.discount_asked:
                if Mongol.horses_bought + int(Mongol.asked_about_seen_stolen) + int(Mongol.theft_asked) >= 3:
                    if player.economy.money < Mongol.horse_price - 200:
                        $ scene_runtime.text = "\"Ты покупатель мой постоянный, так что чего бы не скинуть! По рукам.\"\n\nОднако и со скидкой нужного количества лавэ у вас не оказалось. Смутившись, вы вернулись обратно на центр площади."
                        $ scene_runtime.location_text = scene_runtime.text
                        $ Mongol.horse_price -= 200
                        $ Mongol.discount_asked = True
                        $ main_ui_end_talk_state()
                        return
                    else:
                        $ scene_runtime.text = "\"Ты покупатель мой постоянный, так что чего бы не скинуть! По рукам.\"\n\nОтсчитав Монголу нужное количество лавэ, вы стали счастливым обладателем коняшки со всей сбруей. И не просто коняшки, а голодной коняшки, так как едва очутившись на конюшне лошадка жадно набросилась на овес и сено.\n\n\"А овес ведь нынче дорог,\" запоздало вспомнили вы."
                        $ scene_runtime.location_text = scene_runtime.text
                        $ Mongol.horse_price -= 200
                        $ player.spend_money(Mongol.horse_price)
                        $ player.horse.acquire(RandomStallionNameCode(), Mongol.horse_price, True)
                        $ Mongol.horses_bought += 1
                        $ main_ui_end_talk_state()
                        jump TavernStable
                elif procedural_randint(1, 3 + int(Mongol.asked_about_gypsy), key="procedural:NPC/Secondary/IntMongolTalk.rpy:discount") == 1:
                    $ scene_runtime.text = "\"Сотню могу скинуть. Больше нет, извиняй.\""
                    $ scene_runtime.location_text = scene_runtime.text
                    $ Mongol.horse_price -= 100
                else:
                    $ scene_runtime.text = "\"Не-не чувэрло, извини, не могу скинуть. И так себе в убыток продаю. Совсем у меня с лавэ туго.\""
                    $ scene_runtime.location_text = scene_runtime.text
                $ Mongol.discount_asked = True

            "Беру" if player.economy.money >= Mongol.horse_price:
                $ scene_runtime.text = "Отсчитав Монголу нужное количество лавэ, вы стали счастливым обладателем коняшки со всей сбруей. И не просто коняшки, а голодной коняшки, так как едва очутившись на конюшне лошадка жадно набросилась на овес и сено.\n\n\"А овес ведь нынче дорог,\" запоздало вспомнили вы."
                $ scene_runtime.location_text = scene_runtime.text
                $ player.spend_money(Mongol.horse_price)
                $ player.horse.acquire(RandomStallionNameCode(), Mongol.horse_price, True)
                $ Mongol.horses_bought += 1
                $ main_ui_end_talk_state()
                jump TavernStable

            "Поделиться горем" if not Mongol.theft_asked and player.horse.stolen_days > 0:
                $ scene_runtime.text = "Пока вы думали, Монгол весело напевал задорную песенку. Полностью слов вы разобрать не могли, но время от времени в ней рефреном звучало то \"Спрячь за высоким забором\", то \"Выкраду вместе с забором\".\n\n\"А у меня лошадку кто-то украл...\" огорченно начали вы.\n\n\"Ай-яй, кто же это мог быть?\" сочуственно отозвался Монгол, прекратив напевать. \"Какой негодяй! Как он только посмел! В ночи вскрыть отмычкой замок, надеть лошади на копыта мешки из парусины, чтобы подковы не цокали, и увести. Цыган паршивый! Совсем ворье распоясалось!\"\n\n\"Эй, подожди, а откуда-то ты знаешь что замок отмычкой вскрывали и мешки на копыта надевали? И что это цыган был?\" недоуменно спросили вы.\n\n\"А с чего ты решил, что я знаю?\" немного замялся Монгол. \"Я это, просто догадался. Что тут такого? Лошадь на ночь запирают, значит негодяи вскрыли замок отмычкой. Все же понятно. Ну и цыгане. Мерзкое племя, если где чего украли - то точно они. Как я их ненавижу, чувэрло!\"\n\nОбъяснения Монгола звучали логично, но все-таки какой-то осадок у вас остался."
                $ scene_runtime.location_text = scene_runtime.text
                $ Mongol.theft_asked = True

            "Спросить, почему он до этого скрылся при виде вас" if not Mongol.asked_about_seen_stolen and Mongol.seen_with_stolen_horse and player.horse.stolen_days > 0:
                $ scene_runtime.text = "\"Я? Скрылся?\" искренне удивился Монгол. \"При виде тебя? Да нет, не припомню я такого. А, нет, вспомнил! Я там сборщика пошлин удидел, точно, сборщика. А не хотел я лишний раз платить-то, ведь как я тогда тебе дешевую лошадь продам, если все пошлины платить буду? А тебя я там и вовсе не видел, а ты там был, правда?\" и он уставился на вас неподдельным удивлением от такого невероятного совпадения.\n\n\"Лошадь, что с тобой тогда была, мне еще почему-то знакомой показалась,\" решили уточнить вы. \"Лошадь? Да не припомню ничего в ней особенного, лошадь как лошадь. Лошади, Стефан, они издалека все похожи - четыре ноги и хвост.\"\n\nОбъяснения Монгола звучали логично, но все-таки какой-то осадок у вас остался."
                $ scene_runtime.location_text = scene_runtime.text
                $ Mongol.asked_about_seen_stolen = True

            "Спросить про особый товар" if bool(Clara.merchant_contact_unlocked) and people_to_int(Clara.merchant_contact_month_key, -1) != (int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)):
                call ClaraSecretMerchantMenu

            "Закончить разговор":
                $ main_ui_end_talk_state()
                return


label ClaraSecretMerchantMenu:
    $ renpy.dynamic("_secret_market_month_key")
    $ scene_runtime.text = "Монгол сразу перестает лыбиться так широко и чуть косится по сторонам. \"Если ты от Клариссы, то кое-что редкое у меня для своих есть. Но не шуми, чувэрло. Такое добро показываю только раз в месяц и не каждому подряд.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ _secret_market_month_key = int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)
    while True:
        menu:
            "Купить старинный диван за 600" if threads["claraForestSofa"].num == 2 and not cursed_sofa_installed():
                call ClaraSecretMerchantBuySofa
                if people_to_int(Clara.merchant_contact_month_key, -1) == _secret_market_month_key:
                    return
            "Купить роскошное мыло за 45":
                call ClaraSecretMerchantBuy("luxury_soap_001", 45)
                if people_to_int(Clara.merchant_contact_month_key, -1) == _secret_market_month_key:
                    return
            "Купить пряную настойку за 60":
                call ClaraSecretMerchantBuy("libido_tincture_001", 60)
                if people_to_int(Clara.merchant_contact_month_key, -1) == _secret_market_month_key:
                    return
            "Купить особый гриб за 35":
                call ClaraSecretMerchantBuy("special_mushroom_001", 35)
                if people_to_int(Clara.merchant_contact_month_key, -1) == _secret_market_month_key:
                    return
            "Назад":
                return


label ClaraSecretMerchantBuy(item_id="", price_value=0):
    $ renpy.dynamic("_secret_item", "_secret_price")
    $ _secret_item = str(item_id or "").strip()
    $ _secret_price = max(0, int(price_value or 0))
    if not bool(Clara.merchant_contact_unlocked) or people_to_int(Clara.merchant_contact_month_key, -1) == (int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)):
        $ scene_runtime.text = "Монгол разводит руками: \"На этот месяц все. В другой раз приходи, когда новый товар подвезу.\""
        $ scene_runtime.location_text = scene_runtime.text
        return
    if int(player.economy.money or 0) < _secret_price:
        $ scene_runtime.text = "На такой товар у вас сейчас не хватает денег."
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ player.spend_money(_secret_price)
    $ player.add_item(_secret_item, 1)
    $ Clara.merchant_contact_month_key = int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)
    $ scene_runtime.text = "Монгол быстро прячет деньги и столь же быстро передает вам сверток. \"На этот месяц хватит. Дальше только в следующий раз,\" предупреждает он."
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    return


label ClaraSecretMerchantBuySofa:
    if threads["claraForestSofa"].num != 2 or cursed_sofa_installed():
        $ scene_runtime.text = "Монгол разводит руками: старинного дивана среди его тайного товара больше нет."
        $ scene_runtime.location_text = scene_runtime.text
        return
    if people_to_int(Clara.merchant_contact_month_key, -1) == (int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)):
        $ scene_runtime.text = "На этот месяц Монгол уже показал вам весь доступный особый товар."
        $ scene_runtime.location_text = scene_runtime.text
        return
    if int(player.economy.money or 0) < CLARA_CURSED_SOFA_PRICE:
        $ scene_runtime.text = "На старинный диван у вас не хватает денег. Монгол требует шестьсот мараведи и торговаться отказывается."
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ player.spend_money(CLARA_CURSED_SOFA_PRICE)
    $ _room_add_item_by_id(rooms.get("TavernMain"), "cursed_sofa_001")
    $ Clara.merchant_contact_month_key = int(calendar_v2.cycle or 0) * 100 + int(calendar_v2.period or 0)
    $ scene_runtime.text = "Монгол принимает шестьсот мараведи и обещает доставить тяжелый старинный диван прямо в главную залу вашего трактира. Перед расставанием он советует не пугаться, если мебель начнет ворчать: прежний хозяин тоже жаловался, но потом внезапно уехал из города."
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    return
