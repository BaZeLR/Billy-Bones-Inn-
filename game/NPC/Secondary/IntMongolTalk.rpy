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

            "Закончить разговор":
                $ main_ui_end_talk_state()
                return
