# ================================================================================
# Becky Sherwood talk event labels.
# Availability belongs to beckyThreadList event conditions.
# ================================================================================

label IntBeckyTalkSherwood(girl_name="becky"):
    jump IntBeckyTalk


label story_becky_sherwood_offer_0(girl_name="becky"):
    $ MainTxt = "\"Ага передумал,\" радостно воскликнула вдова. \"Так я и знала, что жадность твою лень пересилит! Рада, что в тебе не ошиблась.\""
    if str(Becky.var.get("TradeOfferText", "") or "") != "":
        $ MainTxt += "\n\n" + str(Becky.var.get("TradeOfferText", "") or "")
    $ CurLocDesc = MainTxt
    $ Becky.var["TradeOffer"] = 1
    $ Becky.finish_talk()
    if thread is not None:
        $ thread.complete()
    jump IntBeckyTalk


label story_becky_sherwood_elves_0(girl_name="becky"):
    $ MainTxt = "\"Так я торговала,\" отозвалась вдовушка. \"Но вот лошадь наша недавно издохла, а на новую у меня сейчас денег нет. Вот и решила, чтоб не дать подработать хорошему человеку.\""
    if GetSexNum("becky", "you", "inside") >= 15:
        $ MainTxt += "\n\n\"Да и не чужой ты мне, ведь сколько твоего семени у меня в середке плещется,\" с пошлым смешком добавила Бекки."
    $ CurLocDesc = MainTxt
    $ Becky.var["AskTradeElf"] = 1
    $ Becky.finish_talk()
    if thread is not None:
        $ thread.complete()
    jump IntBeckyTalk


label story_becky_sherwood_fingal_0(girl_name="becky"):
    $ MainTxt = "\"Ээ, ну нет, в общем-то нет,\" быстро отозвалась Ребекка, слегка покраснев."
    $ CurLocDesc = MainTxt
    $ Becky.var["SherwoodSuspect"] = Becky.var.get("SherwoodSuspect", 0) + 1
    $ Becky.var["FingalClarify"] = 1
    if thread is not None:
        $ thread.complete()
    jump IntBeckyTalk


label story_becky_sherwood_warn_0(girl_name="becky"):
    $ MainTxt = "\"Да, ничего особенного, все нормально будет,\" с наигранной беспечностью отозвалась Ребекка."
    $ CurLocDesc = MainTxt
    $ Becky.var["SherwoodSuspect"] = Becky.var.get("SherwoodSuspect", 0) + 1
    $ Becky.var["SherwoodWarn"] = 2
    if thread is not None:
        $ thread.complete()
    jump IntBeckyTalk


label story_becky_sherwood_road_0(girl_name="becky"):
    $ MainTxt = "\"Дорожка в Куниделл, случаем не через Шервудский лес проходит?\" невинно осведомились вы."
    $ MainTxt += "\n\n\"Через него, это верно. Только какой там лес, от него и не осталось почти ничего,\" заметно нервничая ответила вам Ребекка."
    $ MainTxt += "\n\n\"А там никто, случаем, не пошаливает? Грабеж, все такое?\" еще более невинно спросили вы."
    $ MainTxt += "\n\n\"Ну как тебе сказать,\" смутилась Бекки. \"Дело в том, что да, ты прав, в Куниделл надо ехать через Шервудский лес. Ну, вернее уже не лес, но это не важно.\""
    $ MainTxt += "\n\n\"И что?\""
    $ MainTxt += "\n\n\"Ну вот, собственно, и все. Там уже давно как эти засели, как их там, обездоленные. Говорят, что мол наша добрая герцогиня в их несчастьях и горькой судьбинушке виновата. Раньше от них вреда особого не было, так, собирали по паре десятков мараведи на пропитание. А недавно разухабились, Эдди моего побили, товар отобрали, лошадь отобрали. Так я и решила, ты паренек смышленный, что-нибудь придумаешь. И мне выгода, и тебе прибыток.\""
    $ CurLocDesc = MainTxt
    $ Becky.var["SherwoodSuspect"] = Becky.var.get("SherwoodSuspect", 0) + 10
    $ Becky.var["AdmitSherwood"] = 1
    $ Becky.finish_talk()
    if thread is not None:
        $ thread.complete()
    jump IntBeckyTalk


label story_becky_sherwood_lied_0(girl_name="becky"):
    $ MainTxt = "\"Так я ж не нарочно. Ну, вернее, думала что ты и так справишься, ты ж смышленный, что тебя раньше времени пугать?\""
    $ CurLocDesc = MainTxt
    $ Becky.var["AdmitSherwood"] = 2
    if thread is not None:
        $ thread.complete()
    jump IntBeckyTalk


label story_becky_sherwood_robbed_0(girl_name="becky"):
    $ MainTxt = "\"Ой беда-то какая!\" заохала вдова. \"Это тебя Робин ограбил? Я уж думала он не шалит больше, а оно вот как обернулось. Он, Сирик этакий, Эдди моего ведь тоже ограбил. Даже избил. А тебе вишь, повезло, он тебя и не тронул. Так что можно считать легко отделался.\""
    $ CurLocDesc = MainTxt
    $ Becky.var["AdmitSherwood"] = max(Becky.var.get("AdmitSherwood", 0), 2)
    $ Becky.var["RobbedByRobin"] = Becky.var.get("RobbedByRobin", 0) + 1
    $ Becky.finish_talk()
    if thread is not None:
        $ thread.complete()
    jump IntBeckyTalk


label story_becky_sherwood_howto_0(girl_name="becky"):
    $ MainTxt = "\"Ох, значит Робин этот окаянный там еще. Может ты чего придумаешь? Как бы с ним договориться, больно хорошие деньги эльфы за огурцы платят. А эта их, леди Минетуэль, мне даже сказала как-то, что мол без твоих огурцов я и не знаю, чтобы делала. Все мужики кругом, мол, - эльфы, только огурцы и выручают. До сих пор голову ломаю, что это она в виду имела.\""
    $ CurLocDesc = MainTxt
    $ Becky.var["ConsoleRobbery"] = Becky.var.get("ConsoleRobbery", 0) + 1
    $ Becky.finish_talk()
    if thread is not None:
        $ thread.complete()
    jump IntBeckyTalk


label story_becky_sherwood_warned_0(girl_name="becky"):
    $ MainTxt = "\"Так не виноватая я. Ты и не спрашивал-то особо. А я думала что ты и так справишься, ты ж смышленный, что тебя раньше времени расстраивать? А может энтово Робина там и нет уже? Может он ушел кудайсь? Могло же такое быть? Могло. Вот я и решила тебя не пугать. Ты уж прости меня, дуру.\""
    $ CurLocDesc = MainTxt
    $ Becky.var["RobbedByRobin"] = Becky.var.get("RobbedByRobin", 0) + 1
    if thread is not None:
        $ thread.complete()
    jump IntBeckyTalk
