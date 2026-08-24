# ================================================================================
# Becky Sherwood talk event labels.
# Availability belongs to beckyThreadList event conditions.
# ================================================================================

label story_becky_sherwood_offer_0(girl_name="becky"):
    $ scene_runtime.text = "\"Ага передумал,\" радостно воскликнула вдова. \"Так я и знала, что жадность твою лень пересилит! Рада, что в тебе не ошиблась.\""
    $ scene_runtime.text += "\n\n" + BECKY_TRADE_OFFER_TEXT
    $ scene_runtime.location_text = scene_runtime.text
    $ Becky.trade_offer_stage = 1
    $ Becky.finish_talk()
    return


label story_becky_sherwood_elves_0(girl_name="becky"):
    $ scene_runtime.text = "\"Так я торговала,\" отозвалась вдовушка. \"Но вот лошадь наша недавно издохла, а на новую у меня сейчас денег нет. Вот и решила, чтоб не дать подработать хорошему человеку.\""
    if GetSexNum("becky", "you", "inside") >= 15:
        $ scene_runtime.text += "\n\n\"Да и не чужой ты мне, ведь сколько твоего семени у меня в середке плещется,\" с пошлым смешком добавила Бекки."
    $ scene_runtime.location_text = scene_runtime.text
    $ Becky.asked_about_elf_trade = True
    $ Becky.finish_talk()
    return


label story_becky_sherwood_fingal_0(girl_name="becky"):
    $ scene_runtime.text = "\"Ээ, ну нет, в общем-то нет,\" быстро отозвалась Ребекка, слегка покраснев."
    $ scene_runtime.location_text = scene_runtime.text
    $ Becky.sherwood_suspicion += 1
    $ Becky.fingal_connection_clarified = True
    return


label story_becky_sherwood_warn_0(girl_name="becky"):
    $ scene_runtime.text = "\"Да, ничего особенного, все нормально будет,\" с наигранной беспечностью отозвалась Ребекка."
    $ scene_runtime.location_text = scene_runtime.text
    $ Becky.sherwood_suspicion += 1
    $ Becky.sherwood_warning_stage = 2
    return


label story_becky_sherwood_road_0(girl_name="becky"):
    $ scene_runtime.text = "\"Дорожка в Куниделл, случаем не через Шервудский лес проходит?\" невинно осведомились вы."
    $ scene_runtime.text += "\n\n\"Через него, это верно. Только какой там лес, от него и не осталось почти ничего,\" заметно нервничая ответила вам Ребекка."
    $ scene_runtime.text += "\n\n\"А там никто, случаем, не пошаливает? Грабеж, все такое?\" еще более невинно спросили вы."
    $ scene_runtime.text += "\n\n\"Ну как тебе сказать,\" смутилась Бекки. \"Дело в том, что да, ты прав, в Куниделл надо ехать через Шервудский лес. Ну, вернее уже не лес, но это не важно.\""
    $ scene_runtime.text += "\n\n\"И что?\""
    $ scene_runtime.text += "\n\n\"Ну вот, собственно, и все. Там уже давно как эти засели, как их там, обездоленные. Говорят, что мол наша добрая герцогиня в их несчастьях и горькой судьбинушке виновата. Раньше от них вреда особого не было, так, собирали по паре десятков мараведи на пропитание. А недавно разухабились, Эдди моего побили, товар отобрали, лошадь отобрали. Так я и решила, ты паренек смышленный, что-нибудь придумаешь. И мне выгода, и тебе прибыток.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ Becky.sherwood_suspicion += 10
    $ Becky.admitted_sherwood_stage = 1
    $ Becky.finish_talk()
    return


label story_becky_sherwood_lied_0(girl_name="becky"):
    $ scene_runtime.text = "\"Так я ж не нарочно. Ну, вернее, думала что ты и так справишься, ты ж смышленный, что тебя раньше времени пугать?\""
    $ scene_runtime.location_text = scene_runtime.text
    $ Becky.admitted_sherwood_stage = 2
    return


label story_becky_sherwood_robbed_0(girl_name="becky"):
    $ scene_runtime.text = "\"Ой беда-то какая!\" заохала вдова. \"Это тебя Робин ограбил? Я уж думала он не шалит больше, а оно вот как обернулось. Он, Сирик этакий, Эдди моего ведь тоже ограбил. Даже избил. А тебе вишь, повезло, он тебя и не тронул. Так что можно считать легко отделался.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ Becky.admitted_sherwood_stage = max(Becky.admitted_sherwood_stage, 2)
    $ Becky.robin_robbery_stage += 1
    $ Becky.finish_talk()
    return


label story_becky_sherwood_howto_0(girl_name="becky"):
    $ scene_runtime.text = "\"Ох, значит Робин этот окаянный там еще. Может ты чего придумаешь? Как бы с ним договориться, больно хорошие деньги эльфы за огурцы платят. А эта их, леди Минетуэль, мне даже сказала как-то, что мол без твоих огурцов я и не знаю, чтобы делала. Все мужики кругом, мол, - эльфы, только огурцы и выручают. До сих пор голову ломаю, что это она в виду имела.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ Becky.robbery_consolation_count += 1
    $ Becky.finish_talk()
    return


label story_becky_sherwood_warned_0(girl_name="becky"):
    $ scene_runtime.text = "\"Так не виноватая я. Ты и не спрашивал-то особо. А я думала что ты и так справишься, ты ж смышленный, что тебя раньше времени расстраивать? А может энтово Робина там и нет уже? Может он ушел кудайсь? Могло же такое быть? Могло. Вот я и решила тебя не пугать. Ты уж прости меня, дуру.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ Becky.robin_robbery_stage += 1
    return
