init python:
    def clara_apply_result_counters(result_code):
        result_key = str(result_code or "neutral").strip().lower()
        ClaraVar["lastsocial"] = result_key
        ClaraVar[result_key] = int(ClaraVar.get(result_key, 0) or 0) + 1

    def clara_apply_social_result(interaction_type="talk", gift_item_id=""):
        interaction = str(interaction_type or "talk").strip().lower()
        gift_id = str(gift_item_id or "").strip()
        result_key = clara_social_outcome(interaction, gift_id)

        if interaction == "talk":
            Talked["clara"] = int(Talked.get("clara", 0) or 0) + 1
            TalkedToday["clara"] = int(TalkedToday.get("clara", 0) or 0) + 1
        elif interaction == "flirt":
            Talked["clara"] = int(Talked.get("clara", 0) or 0) + 1
            FlirtedToday["clara"] = int(FlirtedToday.get("clara", 0) or 0) + 1
            ClaraVar["flirt"] = int(ClaraVar.get("flirt", 0) or 0) + 1
        elif interaction == "gift":
            Talked["clara"] = int(Talked.get("clara", 0) or 0) + 1
            GiftedToday["clara"] = int(GiftedToday.get("clara", 0) or 0) + 1

        if result_key == "positive":
            Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + (2 if interaction == "gift" else 1))
            ClaraVar["trust"] = min(20, int(ClaraVar.get("trust", 0) or 0) + 1)
            if interaction == "flirt":
                sluttiness["clara"] = min(100, int(sluttiness.get("clara", 0) or 0) + 1)
        elif result_key == "negative":
            Friends["clara"] = max(0, int(Friends.get("clara", 0) or 0) - (1 if interaction == "flirt" else 0))
            ClaraVar["trust"] = max(0, int(ClaraVar.get("trust", 0) or 0) - 1)

        clara_apply_result_counters(result_key)
        return result_key


label IntClaraTalk(girl_name="clara"):
    $ main_ui_begin_talk_state("Разговор с Клариссой", girl_name)
    $ current_action_title = "Разговор с Клариссой"
    $ current_action_content = None
    $ update_stat_state()
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Кларисса вопросительно смотрит на вас, ожидая, что вы скажете дальше."
        $ CurLocDesc = MainTxt
    call IntClaraTalkRefresh(girl_name)
    return


label IntClaraTalkRefresh(girl_name="clara"):
    $ main_ui_begin_talk_state("Разговор с Клариссой", girl_name)
    $ current_action_title = "Разговор с Клариссой"
    $ current_action_content = None
    $ current_action_items = []
    $ update_stat_state()
    $ current_action_items.append(MenuItem("Осмотреть", Function(NpcActionLookState, girl_name, CurLoc)))
    if TalkedToday.get("clara", 0) == 0:
        $ current_action_items.append(MenuItem("Поболтать с Клариссой о разной фигне.", Function(main_ui_call_label, "IntClaraTalkApply", girl_name, "smalltalk")))
    if str(CurLoc or "") == "MarketPlace" and int(exploration or 0) >= 100 and int(AskedToday.get("clara", 0) or 0) == 0:
        $ current_action_items.append(MenuItem("Проследить за Клариссой по рынку", Function(main_ui_call_label, "IntClaraTalkApply", girl_name, "follow_market")))
    if str(CurLoc or "") == "WineStore" and (story_event_available("WineStore", "clara_talk") or (int(ClaraVar.get("mongol_theft_seen", 0) or 0) == 1 and int(ClaraVar.get("escape_confessed", 0) or 0) == 0)):
        $ current_action_items.append(MenuItem("Осторожно заговорить о ее вечерних делах", Call("story_clara_market_booklet_wine_talk_direct")))

    if FlirtedToday.get("clara", 0) == 0 and clara_can_start_social_events():
        $ current_action_items.append(MenuItem("Заигрывать с Клариссой.", Function(main_ui_call_label, "IntClaraTalkApply", girl_name, "flirt")))
    if GiftedToday.get("clara", 0) == 0 and clara_can_receive_gifts() and clara_has_giftable_entries():
        $ current_action_items.append(MenuItem("Сделать Клариссе подарок.", Function(main_ui_call_label, "IntClaraGiftMenu", girl_name)))
    if int(AskedToday.get("clara", 0) or 0) == 0 and int(Friends.get("clara", 0) or 0) >= 6:
        $ current_action_items.append(MenuItem("Спросить Клариссу о семье", Function(main_ui_call_label, "IntClaraTalkApply", girl_name, "ask_family")))
        $ current_action_items.append(MenuItem("Спросить Клариссу о ней самой", Function(main_ui_call_label, "IntClaraTalkApply", girl_name, "ask_self")))
        if int(ClaraVar.get("drawings_secret_known", 0) or 0) == 1 or int(MelissaVar.get("drawings_found", 0) or 0) == 1:
            $ current_action_items.append(MenuItem("Осторожно заговорить о ее тайных рисунках", Function(main_ui_call_label, "IntClaraTalkApply", girl_name, "ask_drawings")))
    if clara_can_accept_horse_ride(CurLoc):
        $ current_action_items.append(MenuItem("Предложить подвезти Клариссу на коне.", Function(main_ui_call_label, "IntClaraTalkApply", girl_name, "horse_ride")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntClaraGiftMenu(girl_name="clara"):
    $ main_ui_begin_talk_state("Подарок для Клариссы", girl_name)
    $ current_action_title = "Подарок для Клариссы"
    $ current_action_content = None
    $ current_action_items = []
    $ MainTxt = "Вы прикидываете, что из имеющегося при себе может понравиться Клариссе."
    $ CurLocDesc = MainTxt
    python:
        for _gift_row in clara_giftable_entries():
            _gift_caption = str(_gift_row.get("gift_name", "") or "")
            _gift_id = str(_gift_row.get("gift_id", "") or "")
            current_action_items.append(MenuItem(_gift_caption, Function(main_ui_call_label, "IntClaraGiftApply", girl_name, _gift_id)))
    if len(list(current_action_items or [])) <= 0:
        $ MainTxt = "У вас сейчас нет ничего подходящего для подарка."
        $ CurLocDesc = MainTxt
    $ current_action_items.append(MenuItem("Назад", Function(main_ui_call_label, "IntClaraTalkRefresh", girl_name)))
    return


label IntClaraGiftApply(girl_name="clara", gift_id=""):
    python:
        _selected = None
        for _gift_row in clara_giftable_entries():
            if str(_gift_row.get("gift_id", "") or "") == str(gift_id or ""):
                _selected = dict(_gift_row)
                break

        if _selected is None or not clara_remove_gift_entry(_selected):
            MainTxt = "Подарок уже недоступен."
        else:
            _gift_name = str(_selected.get("gift_name", "") or "подарок")
            _result = clara_apply_social_result("gift", str(_selected.get("gift_id", "") or ""))
            if _result == "positive":
                MainTxt = "Вы вручаете Клариссе %s. Ее глаза вспыхивают живым интересом, и она явно довольна вашим выбором." % _gift_name
            elif _result == "neutral":
                MainTxt = "Вы вручаете Клариссе %s. Она принимает подарок вежливо, но без особенного восторга." % _gift_name
            else:
                MainTxt = "Вы предлагаете Клариссе %s, но подарок не производит желаемого впечатления." % _gift_name
        CurLocDesc = MainTxt
    call IntClaraTalkRefresh(girl_name)
    return


label IntClaraTalkApply(girl_name="clara", choice_code=""):
    if str(choice_code or "") == "smalltalk":
        if str(CurLoc or "") in ("ForestClearing", "ForestSpring", "ForestLake"):
            $ _clara_picture = clara_forest_picture(str(CurLoc or ""))
            if str(_clara_picture or "").strip():
                $ ShowImage("", "", _clara_picture)
        if str(CurLoc or "") == "WineStore":
            $ _clara_picture = clara_wine_store_talk_picture()
            if str(_clara_picture or "").strip():
                $ ShowImage("", "", _clara_picture)
        python:
            _result = clara_apply_social_result("talk")
            if _result == "positive":
                MainTxt = "Вы некоторое время болтаете с Клариссой о городских новостях, покупателях и последних сплетнях. Разговор выходит удивительно живым, и Кларисса заметно теплеет к вам."
            elif _result == "neutral":
                MainTxt = "Вы некоторое время болтаете с Клариссой о несущественных вещах. Разговор проходит ровно и без особых откровений."
            else:
                MainTxt = "Вы пытаетесь разговорить Клариссу, но сегодня она отвечает коротко и держится чуть холоднее обычного."
            CurLocDesc = MainTxt
        call IntClaraTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "flirt":
        if not clara_can_start_social_events():
            $ MainTxt = "Вы ловите себя на мысли, что, прежде чем всерьез заигрывать с Клариссой, вам стоит выглядеть и держаться куда увереннее."
            $ CurLocDesc = MainTxt
            call IntClaraTalkRefresh(girl_name)
            return
        if str(CurLoc or "") in ("ForestClearing", "ForestSpring", "ForestLake"):
            $ _clara_picture = clara_forest_picture(str(CurLoc or ""))
            if str(_clara_picture or "").strip():
                $ ShowImage("", "", _clara_picture)
        if str(CurLoc or "") == "WineStore":
            $ _clara_picture = clara_wine_store_flirt_picture()
            if str(_clara_picture or "").strip():
                $ ShowImage("", "", _clara_picture)

        python:
            _result = clara_apply_social_result("flirt")
            if _result == "positive":
                MainTxt = "Вы позволяете себе чуть более смелый и игривый тон. Кларисса отвечает вам лукавой улыбкой и, кажется, начинает смотреть на вас заметно внимательнее."
            elif _result == "neutral":
                MainTxt = "Вы немного флиртуете с Клариссой. Она принимает это скорее как приятную светскую игру, не давая понять ничего определенного."
            else:
                MainTxt = "Вы пытаетесь заигрывать с Клариссой, но она ловко переводит разговор на более безопасные темы."
            CurLocDesc = MainTxt
        call IntClaraTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "horse_ride":
        python:
            _loc = str(CurLoc or "").strip()
            _friends = int(Friends.get("clara", 0) or 0)
            if _loc == "ForestLake" and _friends < 8:
                MainTxt = "Вы предлагаете Клариссе место в седле, но девушка с улыбкой качает головой. «Спасибо, Стефан, но здесь у озера на удивление хорошо. Я еще немного побуду здесь, а потом вернусь сама», - отвечает она."
            else:
                Friends["clara"] = min(20, _friends + 1)
                ClaraVar["trust"] = min(20, int(ClaraVar.get("trust", 0) or 0) + 1)
                CurrentLoc["clara"] = "MarketPlace"
                if _loc == "ForestLake":
                    MainTxt = "Вы предлагаете Клариссе место в седле. Она сначала говорит, что у озера ей очень нравится, но потом все же принимает ваше предложение. По дороге обратно в город девушка заметно расслабляется и благодарит вас за поездку."
                else:
                    MainTxt = "Вы предлагаете Клариссе место в седле и подвозите ее обратно к городу. Девушка сначала смеется над неожиданной затеей, а потом явно начинает смотреть на вас теплее."
            CurLocDesc = MainTxt
        call IntClaraTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ask_family":
        $ AskedToday["clara"] = int(AskedToday.get("clara", 0) or 0) + 1
        $ ClaraVar["trust"] = min(20, int(ClaraVar.get("trust", 0) or 0) + 1)
        $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + 1)
        $ MainTxt = "Вы осторожно спрашиваете Клариссу о ее семье. Девушка сначала держится по-прежнему светски, но потом все же смягчается.\n\n\"У нас дома все устроено правильно и чинно, но иногда от этой правильности устаешь сильнее, чем от любой работы,\" признается она. \"Отец много требует, мать следит за внешними приличиями, а мне все чаще хочется хоть иногда бывать там, где можно говорить свободнее.\""
        $ CurLocDesc = MainTxt
        call IntClaraTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ask_self":
        $ AskedToday["clara"] = int(AskedToday.get("clara", 0) or 0) + 1
        $ ClaraVar["trust"] = min(20, int(ClaraVar.get("trust", 0) or 0) + 1)
        $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + 1)
        $ MainTxt = "Вы просите Клариссу рассказать о себе самой, а не о том, что от нее ждут дома. Она коротко смеется и, поколебавшись, все же отвечает честнее обычного.\n\n\"Я люблю смотреть, как люди ведут дела и как один и тот же город меняется в зависимости от того, с кем ты говоришь. Наверное, мне нравится наблюдать и делать выводы. Просто дома не всякому понравится, если девушка слишком много замечает,\" говорит Кларисса."
        $ CurLocDesc = MainTxt
        call IntClaraTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ask_drawings":
        $ AskedToday["clara"] = int(AskedToday.get("clara", 0) or 0) + 1
        $ ClaraVar["trust"] = min(20, int(ClaraVar.get("trust", 0) or 0) + 2)
        $ Friends["clara"] = min(20, int(Friends.get("clara", 0) or 0) + 1)
        $ MainTxt = "Вы осторожно даете Клариссе понять, что знаете о ее тайных непристойных рисунках и не собираетесь поднимать из-за этого шум. Она сперва цепенеет, но потом, поняв ваш тон, только шумно выдыхает.\n\n\"Дома за такое меня бы живьем съели,\" признается она. \"Отец требует приличий, мать — судьбы по правилам, а мне иногда хочется хотя бы на бумаге жить не так, как велено. Потому я и наблюдаю за людьми, и слушаю лишнее. Иначе совсем задохнешься в чужих ожиданиях.\""
        $ CurLocDesc = MainTxt
        call IntClaraTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "follow_market":
        $ AskedToday["clara"] = int(AskedToday.get("clara", 0) or 0) + 1
        $ ClaraVar["trust"] = min(20, int(ClaraVar.get("trust", 0) or 0) + 1)
        $ MainTxt = "Вы не навязываетесь Клариссе разговором, а просто держитесь чуть поодаль и смотрите, куда она направится дальше. Девушка делает круг по рыночным рядам, будто проверяя, нет ли за ней чужих глаз, а затем уверенно уходит к знакомому входу в винную лавку Легаре.\n\nПохоже, даже на рынке Кларисса все время держит в уме путь обратно в винную лавку семьи."
        $ CurLocDesc = MainTxt
        $ CurrentLoc["clara"] = "WineStore"
        call IntClaraTalkRefresh(girl_name)
        return

    $ main_ui_end_talk_state()
    return
