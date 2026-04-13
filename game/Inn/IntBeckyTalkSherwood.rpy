label IntBeckyTalkSherwood(girl_name="becky"):
    $ _becky_sherwood_name = str(girl_name or "becky")
    $ main_ui_begin_talk_state("Шервуд", _becky_sherwood_name)
    $ current_action_title = "Шервуд"
    $ current_action_content = None
    $ MainTxt = "Бекки готова обсудить с вами историю с Шервудом."
    $ CurLocDesc = MainTxt
    call IntBeckyTalkSherwoodRefresh(_becky_sherwood_name)
    return


label IntBeckyTalkSherwoodRefresh(girl_name="becky"):
    $ main_ui_begin_talk_state("Шервуд", girl_name)
    $ current_action_title = "Шервуд"
    $ current_action_content = None
    $ current_action_items = []

    if Talked.get(girl_name, 0) < 2 and BeckyVar.get("TradeOffer", 0) == 2:
        $ current_action_items.append(MenuItem("Насчет твоего предложения, в чем там все-таки дело?", Function(main_ui_call_label, "IntBeckyTalkSherwoodApply", girl_name, "offer")) )
    if Talked.get(girl_name, 0) < 2 and BeckyVar.get("TradeOffer", 0) == 1 and BeckyVar.get("AskTradeElf", 0) == 0:
        $ current_action_items.append(MenuItem("А чего ты сама с эльфами не торгуешь?", Function(main_ui_call_label, "IntBeckyTalkSherwoodApply", girl_name, "elves")) )
    if BeckyVar.get("TradeOffer", 0) == 1 and EddieVar.get("FingalTalk", 0) > 0 and BeckyVar.get("FingalClarify", 0) == 0 and BeckyVar.get("AdmitSherwood", 0) == 0:
        $ current_action_items.append(MenuItem("А твое предложеньице с фингалом у твоего сынка не связанно, случаем?", Function(main_ui_call_label, "IntBeckyTalkSherwoodApply", girl_name, "fingal"))) 
    if BeckyVar.get("TradeOffer", 0) == 1 and BeckyVar.get("SherwoodWarn", 0) == 1 and BeckyVar.get("AdmitSherwood", 0) == 0:
        $ current_action_items.append(MenuItem("О какой-такой загвоздке ты говорила?", Function(main_ui_call_label, "IntBeckyTalkSherwoodApply", girl_name, "warn"))) 
    if Talked.get(girl_name, 0) < 2 and BeckyVar.get("TradeOffer", 0) == 1 and BeckyVar.get("AdmitSherwood", 0) == 0 and BeckyVar.get("KnowSherwood", 0) == 1:
        $ current_action_items.append(MenuItem("Насчет дороги в Куниделл", Function(main_ui_call_label, "IntBeckyTalkSherwoodApply", girl_name, "road"))) 
    if BeckyVar.get("TradeOffer", 0) == 1 and BeckyVar.get("AdmitSherwood", 0) == 1:
        $ current_action_items.append(MenuItem("Так что же ты меня дурила-то?", Function(main_ui_call_label, "IntBeckyTalkSherwoodApply", girl_name, "lied"))) 
    if Talked.get(girl_name, 0) < 2 and BeckyVar.get("RobbedByRobin", 0) == 1:
        $ current_action_items.append(MenuItem("Меня ограбили!!!", Function(main_ui_call_label, "IntBeckyTalkSherwoodApply", girl_name, "robbed"))) 
    if Talked.get(girl_name, 0) < 2 and BeckyVar.get("ConsoleRobbery", 0) == 0 and BeckyVar.get("RobbedByRobin", 0) >= 2:
        $ current_action_items.append(MenuItem("Так как мне в Куниделл попасть-то?", Function(main_ui_call_label, "IntBeckyTalkSherwoodApply", girl_name, "howto"))) 
    if BeckyVar.get("RobbedByRobin", 0) == 2 and BeckyVar.get("AdmitSherwood", 0) == 0:
        $ current_action_items.append(MenuItem("Так что ж ты меня не предупредила-то?", Function(main_ui_call_label, "IntBeckyTalkSherwoodApply", girl_name, "warned"))) 

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_call_label, "IntBeckyTalkRefresh", girl_name)))
    return


label IntBeckyTalkSherwoodApply(girl_name="becky", choice_code=""):
    if str(choice_code or "") == "offer":
        $ MainTxt = "Ага передумал, радостно воскликнула вдова. Так я и знала, что жадность твою лень пересилит! Рада, что в тебе не ошиблась."
        if str(BeckyVar.get("TradeOfferText", "") or "") != "":
            $ MainTxt += "\n\n" + str(BeckyVar.get("TradeOfferText", "") or "")
        $ BeckyVar["TradeOffer"] = 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
    elif str(choice_code or "") == "elves":
        $ MainTxt = "Так я торговала, отозвалась вдовушка. Но вот лошадь наша недавно издохла, а на новую у меня сейчас денег нет. Вот и решила, чтоб не дать подработать хорошему человеку."
        if GetSexNum("becky", "you", "inside") >= 15:
            $ MainTxt += "\n\nДа и не чужой ты мне, ведь сколько твоего семени у меня в середке плещется, со пошлым смешком добавила Бекки."
        $ BeckyVar["AskTradeElf"] = 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
    elif str(choice_code or "") == "fingal":
        $ MainTxt = "Ээ, ну нет, в общем-то нет, быстро отозвалась Ребекка, слегка покраснев."
        $ BeckyVar["SherwoodSuspect"] = BeckyVar.get("SherwoodSuspect", 0) + 1
        $ BeckyVar["FingalClarify"] = 1
    elif str(choice_code or "") == "warn":
        $ MainTxt = "Да, ничего особенного, все нормально будет, с наигранной беспечностью отозвалась Ребекка."
        $ BeckyVar["SherwoodSuspect"] = BeckyVar.get("SherwoodSuspect", 0) + 1
        $ BeckyVar["SherwoodWarn"] = 2
    elif str(choice_code or "") == "road":
        $ MainTxt = "Дорожка в Куниделл, случаем не через Шервудский лес проходит?\n\nЧерез него, это верно. Только какой там лес, от него и не осталось почти ничего, заметно нервничая ответила вам Ребекка."
        $ MainTxt += "\n\nНу как тебе сказать, смутилась Бекки."
        $ MainTxt += "\n\nДело в том, что да, ты прав, в Куниделл надо ехать через Шервудский лес. Ну, вернее уже не лес, но это не важно. И что? Ну вот, собственно, и все. Там уже давно как эти засели, как их там, обездоленные."
        $ MainTxt += "\n\nГоворят, что мол наша добрая герцогиня в их несчастьях и горькой судьбинушке виновата. Раньше от них вреда особого не было, так, собирали по паре десятков мараведи на пропитание. А недавно разухабились, сыночка моего ненаглядного побили, товар отобрали, лошадь отобрали."
        $ MainTxt += "\n\nТак я и решила, ты паренек смышленный, что-нибудь придумаешь. И мне выгода, и тебе прибыток."
        $ BeckyVar["SherwoodSuspect"] = BeckyVar.get("SherwoodSuspect", 0) + 10
        $ BeckyVar["AdmitSherwood"] = 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
    elif str(choice_code or "") == "lied":
        $ MainTxt = "Так я ж не нарочно. Ну, вернее, думала что ты и так справишься, ты ж смышленный, что тебя раньше времени пугать?"
        $ BeckyVar["AdmitSherwood"] = 2
    elif str(choice_code or "") == "robbed":
        $ MainTxt = "Ой беда-то какая!\n\nзаохала вдова."
        $ MainTxt += "\n\nЭто тебя Робин ограбил? Я уж думала он не шалит больше, а оно вот как обернулось. Он, Сирик этакий, сыночка моего ведь тоже ограбил. Даже избил. А тебе вишь, повезло, он тебя и не тронул. Так что можно считать легко отделался."
        $ BeckyVar["AdmitSherwood"] = max(BeckyVar.get("AdmitSherwood", 0), 2)
        $ BeckyVar["RobbedByRobin"] = BeckyVar.get("RobbedByRobin", 0) + 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
    elif str(choice_code or "") == "howto":
        $ MainTxt = "Ох, значит Робин этот окаянный там еще. Может ты чего придумаешь? Как бы с ним договориться, больно хорошие деньги эльфы за огурцы платят."
        $ MainTxt += "\n\nА эта их, леди Минетуэль, мне даже сказала как-то, что мол без твоих огурцов я и не знаю, чтобы делала. Все мужики кругом, мол, - эльфы, только огурцы и выручают. До сих пор голову ломаю, что это она в виду имела."
        $ BeckyVar["ConsoleRobbery"] = BeckyVar.get("ConsoleRobbery", 0) + 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
    elif str(choice_code or "") == "warned":
        $ MainTxt = "Так не виноватая я. Ты и не спрашивал-то особо. А я думала что ты и так справишься, ты ж смышленный, что тебя раньше времени расстраивать? А может энтово Робина там и нет уже? Может он ушел кудайсь? Могло же такое быть? Могло. Вот я и решила тебя не пугать. Ты уж прости меня, дуру."
        $ BeckyVar["RobbedByRobin"] = BeckyVar.get("RobbedByRobin", 0) + 1
    else:
        call IntBeckyTalkRefresh(girl_name)
        return

    $ CurLocDesc = MainTxt
    call IntBeckyTalkSherwoodRefresh(girl_name)
    return
