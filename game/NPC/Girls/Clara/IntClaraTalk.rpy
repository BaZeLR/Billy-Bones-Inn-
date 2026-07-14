    if str(choice_code or "") == "talk":
        call TalkSystemSmallTalkMenu(girl_name)
        return
    if str(choice_code or "") == "flirt":
        call TalkSystemFlirtAttempt(girl_name)
        return
label IntClaraTalkApply(girl_name="clara", choice_code=""):
    if str(choice_code or "") == "smalltalk":
        call TalkSystemSmallTalkMenu(girl_name)
        return

    if str(choice_code or "") == "flirt":
        if str(CurLoc or "") in ("ForestClearing", "ForestSpring", "ForestLake"):
            $ _clara_picture = clara_forest_picture(str(CurLoc or ""))
            if str(_clara_picture or "").strip():
                vscene _clara_picture
        if str(CurLoc or "") == "WineStore":
            $ _clara_picture = clara_wine_store_flirt_picture()
            if str(_clara_picture or "").strip():
                vscene _clara_picture

        call TalkSystemFlirtAttempt(girl_name)
        return

    if str(choice_code or "") == "horse_ride":
        python:
            _loc = str(CurLoc or "").strip()
            if _loc == "ForestLake" and int(Clara.rel or 0) < 8:
                MainTxt = "Вы предлагаете Клариссе место в седле, но девушка с улыбкой качает головой. «Спасибо, Стефан, но здесь у озера на удивление хорошо. Я еще немного побуду здесь, а потом вернусь сама», - отвечает она."
            else:
                Clara.change_social(friend_delta=1)
                Clara.trust = min(20, int(Clara.trust or 0) + 1)
                Clara.var["trust"] = int(Clara.trust or 0)
                Clara.current_location = "MarketPlace"
                if _loc == "ForestLake":
                    MainTxt = "Вы предлагаете Клариссе место в седле. Она сначала говорит, что у озера ей очень нравится, но потом все же принимает ваше предложение. По дороге обратно в город девушка заметно расслабляется и благодарит вас за поездку."
                else:
                    MainTxt = "Вы предлагаете Клариссе место в седле и подвозите ее обратно к городу. Девушка сначала смеется над неожиданной затеей, а потом явно начинает смотреть на вас теплее."
            CurLocDesc = MainTxt
        call IntClaraTalkMenu(girl_name)
        call IntClaraTalkMenu(girl_name)
    return

    if str(choice_code or "") == "ask_family":
        $ Clara.mark_asked()
        $ Clara.mark_talked()
        $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
        $ Clara.var["trust"] = int(Clara.trust or 0)
        $ Clara.change_social(friend_delta=1)
        $ MainTxt = "Вы осторожно спрашиваете Клариссу о ее семье. Девушка сначала держится по-прежнему светски, но потом все же смягчается.\n\n\"У нас дома все устроено правильно и чинно, но иногда от этой правильности устаешь сильнее, чем от любой работы,\" признается она. \"Отец много требует, мать следит за внешними приличиями, а мне все чаще хочется хоть иногда бывать там, где можно говорить свободнее.\""
        $ CurLocDesc = MainTxt
        call IntClaraTalkMenu(girl_name)
        return

    if str(choice_code or "") == "ask_self":
        $ Clara.mark_asked()
        $ Clara.mark_talked()
        $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
        $ Clara.var["trust"] = int(Clara.trust or 0)
        $ Clara.change_social(friend_delta=1)
        $ MainTxt = "Вы просите Клариссу рассказать о себе самой, а не о том, что от нее ждут дома. Она коротко смеется и, поколебавшись, все же отвечает честнее обычного.\n\n\"Я люблю смотреть, как люди ведут дела и как один и тот же город меняется в зависимости от того, с кем ты говоришь. Наверное, мне нравится наблюдать и делать выводы. Просто дома не всякому понравится, если девушка слишком много замечает,\" говорит Кларисса."
        $ CurLocDesc = MainTxt
        call IntClaraTalkMenu(girl_name)
        return

    if str(choice_code or "") == "ask_water_pump":
        $ Clara.mark_asked()
        $ Clara.mark_talked()
        $ Clara.var["old_water_pump_hint_seen"] = 1
        $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
        $ Clara.var["trust"] = int(Clara.trust or 0)
        $ Clara.change_social(friend_delta=1)
        $ MainTxt = "Кларисса, чуть усмехнувшись, признает, что в городе есть места, куда люди ходят не за водой и не за прогулкой.\n\n\"У старой водокачки, за лесной тропой, часто встречаются те, кому не хочется лишних глаз,\" говорит она. \"Если после того, что ты уже слышал с чердака, тебе все еще нужны доказательства, ищи не на главной дороге. Секреты любят обходные тропы.\""
        $ CurLocDesc = MainTxt
        call IntClaraTalkMenu(girl_name)
        return

    if str(choice_code or "") == "ask_drawings":
        $ Clara.mark_asked()
        $ Clara.mark_talked()
        $ Clara.trust = min(20, int(Clara.trust or 0) + 2)
        $ Clara.var["trust"] = int(Clara.trust or 0)
        $ Clara.change_social(friend_delta=1)
        $ MainTxt = "Вы осторожно даете Клариссе понять, что знаете о ее тайных непристойных рисунках и не собираетесь поднимать из-за этого шум. Она сперва цепенеет, но потом, поняв ваш тон, только шумно выдыхает.\n\n\"Дома за такое меня бы живьем съели,\" признается она. \"Отец требует приличий, мать — судьбы по правилам, а мне иногда хочется хотя бы на бумаге жить не так, как велено. Потому я и наблюдаю за людьми, и слушаю лишнее. Иначе совсем задохнешься в чужих ожиданиях.\""
        $ CurLocDesc = MainTxt
        call IntClaraTalkMenu(girl_name)
        return

    if str(choice_code or "") == "follow_market":
        $ Clara.mark_asked()
        $ Clara.mark_talked()
        $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
        $ Clara.var["trust"] = int(Clara.trust or 0)
        $ MainTxt = "Вы не навязываетесь Клариссе разговором, а просто держитесь чуть поодаль и смотрите, куда она направится дальше. Девушка делает круг по рыночным рядам, будто проверяя, нет ли за ней чужих глаз, а затем уверенно уходит к знакомому входу в винную лавку Легаре.\n\nПохоже, даже на рынке Кларисса все время держит в уме путь обратно в винную лавку семьи."
        $ CurLocDesc = MainTxt
        $ Clara.current_location = "WineStore"
        call IntClaraTalkMenu(girl_name)
        return

    $ main_ui_end_talk_state()
    return