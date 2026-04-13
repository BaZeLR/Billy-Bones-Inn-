label MongolTalk:
    $ current_action_title = "Монгол"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Call("MongolTalkApply", "look")))

    if MongolVar['GypsyAsk'] == 0:
        $ current_action_items.append(MenuItem("А ты цыган?", Call("MongolTalkApply", "gypsy")))

    if MongolVar['ZimmerKnow'] == 1 and MongolVar['AskPriceIncr'] == 0:
        $ current_action_items.append(MenuItem("А чего дороже-то продаешь, раньше же 1000 было?", Call("MongolTalkApply", "price")))

    if MongolVar['DiscountAsk'] == 0:
        $ current_action_items.append(MenuItem("Пару сотен скинешь?", Call("MongolTalkApply", "discount")))

    if money >= MongolVar['HorsePrice']:
        $ current_action_items.append(MenuItem("Беру", Call("MongolTalkApply", "buy")))

    if MongolVar['TheftAsk'] == 0 and StolenHorseDays > 0:
        $ current_action_items.append(MenuItem("Поделиться горем", Call("MongolTalkApply", "theft")))

    if MongolVar['AskSawStolen'] == 0 and MongolVar['SawStolen'] == 1 and StolenHorseDays > 0:
        $ current_action_items.append(MenuItem("Спросить, почему он до этого скрылся при виде вас", Call("MongolTalkApply", "saw_stolen")))

    $ current_action_items.append(MenuItem("Закончить разговор", Call("MarketPlaceRestore")))
    return


label MongolTalkApply(topic_code=""):
    if topic_code == "look":
        $ MainTxt = "Монгол - торговец лошадьми. Он одет в красную рубаху, широкие штаны и высокие сапоги. В ухе у него серьга а на голове цветная косынка. Он держит за повод оседланного жеребца."
        $ CurLocDesc = MainTxt
        call ShowImageSeq("mongol", "", "portrait", 3)
        call MongolTalk
        return

    if topic_code == "gypsy":
        $ MainTxt = "\"Я? Цыган?\" удивился вашему вопросу Монгол. \"Да какой же я цыган, что во мне цыганского? Да я этих цыган просто ненавижу! Я их, если хочешь знать, просто терпеть не могу! Ворье и жулье они! А я честный лошадиный барышник. Даже слишком честный, не поверишь, себе в убыток торгую!\"\n\nВ последнем своем предположении Монгол был прав, вы почему-то ему не поверили."
        $ CurLocDesc = MainTxt
        $ MongolVar['GypsyAsk'] = 1
        call MongolTalk
        return

    if topic_code == "price":
        $ MainTxt = "\"Да я бы и рад подешевле, но ты войди в мое положение! Мне семью кормить надо, а тут еще стража денег с нас, якобы за защиту, требует. Десятник этот картавый целый стольник потребовал, иначе, мол, говорит, нельзя тебе здесь лошадьми торговать. Мол поступлю тогда с тобой по всей строгости закона. А ведь сам знаешь, что за конокра.., в смысле за тороговлю лошадьми без лицензии полагается.\""
        $ CurLocDesc = MainTxt
        $ MongolVar['AskPriceIncr'] = 1
        call MongolTalk
        return

    if topic_code == "discount":
        if MongolVar['HorsesBought'] + MongolVar['AskSawStolen'] + MongolVar['TheftAsk'] >= 3:
            if money < MongolVar['HorsePrice'] - 200:
                $ MainTxt = "\"Ты покупатель мой постоянный, так что чего бы не скинуть! По рукам.\"\n\nОднако и со скидкой нужного количества лавэ у вас не оказалось. Смутившись, вы вернулись обратно на центр площади."
                $ CurLocDesc = MainTxt
                $ MongolVar['HorsePrice'] -= 200
                $ MongolVar['DiscountAsk'] = 1
                call MarketPlaceRestore
                return
            else:
                $ MainTxt = "\"Ты покупатель мой постоянный, так что чего бы не скинуть! По рукам.\"\n\nОтсчитав Монголу нужное количество лавэ, вы стали счастливым обладателем коняшки со всей сбруей. И не просто коняшки, а голодной коняшки, так как едва очутившись на конюшне лошадка жадно набросилась на овес и сено.\n\n\"А овес ведь нынче дорог,\" запоздало вспомнили вы."
                $ CurLocDesc = MainTxt
                $ MongolVar['HorsePrice'] -= 200
                $ money -= MongolVar['HorsePrice']
                $ MyStallion = renpy.python.py_eval("RandomStallionNameCode()")
                $ HorseSaddled = 1
                $ MongolVar['HorsesBought'] += 1
                hide screen girl_card_overlay
                hide screen player_card_overlay
                hide screen main_ui
                jump TavernStable
        elif renpy.random.randint(1, 3 + MongolVar['GypsyAsk']) == 1:
            $ MainTxt = "\"Сотню могу скинуть. Больше нет, извиняй.\""
            $ CurLocDesc = MainTxt
            $ MongolVar['HorsePrice'] -= 100
        else:
            $ MainTxt = "\"Не-не чувэрло, извини, не могу скинуть. И так себе в убыток продаю. Совсем у меня с лавэ туго.\""
            $ CurLocDesc = MainTxt
        $ MongolVar['DiscountAsk'] = 1
        call MongolTalk
        return

    if topic_code == "buy":
        $ MainTxt = "Отсчитав Монголу нужное количество лавэ, вы стали счастливым обладателем коняшки со всей сбруей. И не просто коняшки, а голодной коняшки, так как едва очутившись на конюшне лошадка жадно набросилась на овес и сено.\n\n\"А овес ведь нынче дорог,\" запоздало вспомнили вы."
        $ CurLocDesc = MainTxt
        $ money -= MongolVar['HorsePrice']
        $ MyStallion = renpy.python.py_eval("RandomStallionNameCode()")
        $ HorseSaddled = 1
        $ MongolVar['HorsesBought'] += 1
        hide screen girl_card_overlay
        hide screen player_card_overlay
        hide screen main_ui
        jump TavernStable

    if topic_code == "theft":
        $ MainTxt = "Пока вы думали, Монгол весело напевал задорную песенку. Полностью слов вы разобрать не могли, но время от времени в ней рефреном звучало то \"Спрячь за высоким забором\", то \"Выкраду вместе с забором\".\n\n\"А у меня лошадку кто-то украл...\" огорченно начали вы.\n\n\"Ай-яй, кто же это мог быть?\" сочуственно отозвался Монгол, прекратив напевать. \"Какой негодяй! Как он только посмел! В ночи вскрыть отмычкой замок, надеть лошади на копыта мешки из парусины, чтобы подковы не цокали, и увести. Цыган паршивый! Совсем ворье распоясалось!\"\n\n\"Эй, подожди, а откуда-то ты знаешь что замок отмычкой вскрывали и мешки на копыта надевали? И что это цыган был?\" недоуменно спросили вы.\n\n\"А с чего ты решил, что я знаю?\" немного замялся Монгол. \"Я это, просто догадался. Что тут такого? Лошадь на ночь запирают, значит негодяи вскрыли замок отмычкой. Все же понятно. Ну и цыгане. Мерзкое племя, если где чего украли - то точно они. Как я их ненавижу, чувэрло!\"\n\nОбъяснения Монгола звучали логично, но все-таки какой-то осадок у вас остался."
        $ CurLocDesc = MainTxt
        $ MongolVar['TheftAsk'] = 1
        call MongolTalk
        return

    $ MainTxt = "\"Я? Скрылся?\" искренне удивился Монгол. \"При виде тебя? Да нет, не припомню я такого. А, нет, вспомнил! Я там сборщика пошлин удидел, точно, сборщика. А не хотел я лишний раз платить-то, ведь как я тогда тебе дешевую лошадь продам, если все пошлины платить буду? А тебя я там и вовсе не видел, а ты там был, правда?\" и он уставился на вас неподдельным удивлением от такого невероятного совпадения.\n\n\"Лошадь, что с тобой тогда была, мне еще почему-то знакомой показалась,\" решили уточнить вы. \"Лошадь? Да не припомню ничего в ней особенного, лошадь как лошадь. Лошади, Стефан, они издалека все похожи - четыре ноги и хвост.\"\n\nОбъяснения Монгола звучали логично, но все-таки какой-то осадок у вас остался."
    $ CurLocDesc = MainTxt
    $ MongolVar['AskSawStolen'] = 1
    call MongolTalk
    return
