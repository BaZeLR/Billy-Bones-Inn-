label IntBeckyTalk(girl_name="becky"):
    $ _becky_name = str(girl_name or "becky")
    $ main_ui_begin_talk_state("Разговор с Бекки", _becky_name)
    $ current_action_title = "Разговор с Бекки"
    $ current_action_content = None
    python:
        _becky_picture = str(girl_card_portrait_path(_becky_name) or "").strip()
        if _becky_picture and renpy.loadable(_becky_picture):
            scene_image = _becky_picture
            _layout_last_picture = _becky_picture
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Бекки внимательно смотрит на вас, ожидая, что вы захотите обсудить."
        $ CurLocDesc = MainTxt
    call IntBeckyTalkRefresh(_becky_name)
    return


label IntBeckyTalkRefresh(girl_name="becky"):
    $ main_ui_begin_talk_state("Разговор с Бекки", girl_name)
    $ current_action_title = "Разговор с Бекки"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Function(show_girl_card_main_ui_state, girl_name)))
    $ current_action_items.append(MenuItem("Поболтать со вдовой Блэнкеншип о разной фигне", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "smalltalk")))

    if Friends.get(girl_name, 0) >= 3:
        $ current_action_items.append(MenuItem("Поболтать с Бекки о более личных вещах", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "personal")))

    if becky_dress_change_has_options(girl_name):
        $ current_action_items.append(MenuItem("Поговорить с Бекки об одежде", Function(main_ui_call_label, "IntBeckyDressChange", girl_name)))

    if BeckyVar.get("SawIngaFuck", 0) == 1 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Спросить Бекки про дочку с женихом", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "inga1")))
    if BeckyVar.get("SawIngaFuck", 0) == 2 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Распросить еще про дочку", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "inga2")))
    if BeckyVar.get("SawIngaFuck", 0) == 3 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Распросить про Лукаса, жениха Ингенборг", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "lucas")))

    if BeckyVar.get("husbandtalk", 0) == 1 and Friends.get(girl_name, 0) > 13 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Распросить Бекки про ее покойного мужа", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "husband1")))
    if BeckyVar.get("husbandtalk", 0) == 2 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Распросить еще про Эрика", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "husband2")))
    if BeckyVar.get("husbandtalk", 0) == 3 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Узнать что сталось с другими подружками Эрика", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "husband3")))
    if BeckyVar.get("husbandtalk", 0) == 4 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Спросить про остальных подружек Эрика", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "husband4")))

    if BeckyVar.get("eddietalk", 0) == 0 and Friends.get(girl_name, 0) > 6 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Спросить про ее сына Эдди", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "eddie1")))
    if EddieVar.get("TalkedAboutGeorgett", 0) > 0 and BeckyVar.get("husbandtalk", 0) > 0 and BeckyVar.get("eddietalk", 0) > 0 and Friends.get(girl_name, 0) > 8 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Рассказать про игру Эдди и Жоржетты", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "eddie2")))

    if BeckyVar.get("visitedhome", 0) == 2 and Friends.get(girl_name, 0) > 12 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Попробовать напросится в гости", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "invite")))
    if BeckyVar.get("TimesVisited", 0) > 0 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Спросить о прошлом визите в гости", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "lastvisit")))

    if BeckyVar.get("visitedhome", 0) >= 3 and (EddieVar.get("SawMomSex", 0) > 0 or BeckyVar.get("HomeSex", 0) > 0) and BeckyVar.get("visitedhome", 0) < 7 and BeckyVar.get("EddieTryToFuck", 0) < 4 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Указать Бекки на поведение ее сына", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "eddie3")))
    if BeckyVar.get("EddieGeorg", 0) > 1 and BeckyVar.get("visitedhome", 0) < 7 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Рассказать что Эдди требует, чтобы Жоржетта изображала Бекки", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "eddie4")))
    if BeckyVar.get("GeorgMention", 0) == 1 and BeckyVar.get("visitedhome", 0) < 7 and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Возмутиться поведением Эдди", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "eddie5")))
        $ current_action_items.append(MenuItem("Посоветовать Бекки быть повнимательнее к любым нуждам сына", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "eddie6")))
    if ((BeckyVar.get("EddieTryToFuck", 0) == 4 and BeckyVar.get("AskedEddieFuck", 0) == 0) or (BeckyVar.get("visitedhome", 0) >= 7 and BeckyVar.get("AskedEddieFuck", 0) < 2)) and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Поговорить с Бекки об Эдди", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "eddie7")))

    if Talked.get(girl_name, 0) < 2 and Friends.get(girl_name, 0) >= 8 and pregnancy.get(girl_name, 0) >= 120:
        $ _dad_phrase = DaddyAskBuildPhrase(girl_name)
        if _dad_phrase != "":
            $ current_action_items.append(MenuItem("Спросить, знает ли она от кого затяжелела", Function(main_ui_call_label, "IntBeckyTalkApply", girl_name, "pregnancy")))

    if (
        (Talked.get(girl_name, 0) < 2 and BeckyVar.get("TradeOffer", 0) == 2) or
        (Talked.get(girl_name, 0) < 2 and BeckyVar.get("TradeOffer", 0) == 1 and BeckyVar.get("AskTradeElf", 0) == 0) or
        (BeckyVar.get("TradeOffer", 0) == 1 and EddieVar.get("FingalTalk", 0) > 0 and BeckyVar.get("FingalClarify", 0) == 0 and BeckyVar.get("AdmitSherwood", 0) == 0) or
        (BeckyVar.get("TradeOffer", 0) == 1 and BeckyVar.get("SherwoodWarn", 0) == 1 and BeckyVar.get("AdmitSherwood", 0) == 0) or
        (Talked.get(girl_name, 0) < 2 and BeckyVar.get("TradeOffer", 0) == 1 and BeckyVar.get("AdmitSherwood", 0) == 0 and BeckyVar.get("KnowSherwood", 0) == 1) or
        (BeckyVar.get("TradeOffer", 0) == 1 and BeckyVar.get("AdmitSherwood", 0) == 1) or
        (Talked.get(girl_name, 0) < 2 and BeckyVar.get("RobbedByRobin", 0) == 1) or
        (Talked.get(girl_name, 0) < 2 and BeckyVar.get("ConsoleRobbery", 0) == 0 and BeckyVar.get("RobbedByRobin", 0) >= 2) or
        (BeckyVar.get("RobbedByRobin", 0) == 2 and BeckyVar.get("AdmitSherwood", 0) == 0)
    ):
        $ current_action_items.append(MenuItem("Обсудить дела с Шервудом", Function(main_ui_call_label, "IntBeckyTalkSherwood", girl_name)))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(grocery_store_restore_scene_state)))
    return


label IntBeckyTalkApply(girl_name="becky", choice_code=""):
    if str(choice_code or "") == "inspect":
        call GirlsDesc("becky")
        call IntBeckyTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "pregnancy":
        $ MainTxt = DaddyAskBuildPhrase(girl_name)
        if str(MainTxt or "") != "":
            $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntBeckyTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "smalltalk":
        call _int_becky_talk_smalltalk(girl_name)
    elif str(choice_code or "") == "personal":
        call _int_becky_talk_personal(girl_name)
    elif str(choice_code or "") == "inga1":
        call _int_becky_talk_inga1(girl_name)
    elif str(choice_code or "") == "inga2":
        call _int_becky_talk_inga2(girl_name)
    elif str(choice_code or "") == "lucas":
        call _int_becky_talk_lucas(girl_name)
    elif str(choice_code or "") == "husband1":
        call _int_becky_talk_husband1(girl_name)
    elif str(choice_code or "") == "husband2":
        call _int_becky_talk_husband2(girl_name)
    elif str(choice_code or "") == "husband3":
        call _int_becky_talk_husband3(girl_name)
    elif str(choice_code or "") == "husband4":
        call _int_becky_talk_husband4(girl_name)
    elif str(choice_code or "") == "eddie1":
        call _int_becky_talk_eddie1(girl_name)
    elif str(choice_code or "") == "eddie2":
        call _int_becky_talk_eddie2(girl_name)
    elif str(choice_code or "") == "invite":
        call _int_becky_talk_invite(girl_name)
    elif str(choice_code or "") == "lastvisit":
        call _int_becky_talk_lastvisit(girl_name)
    elif str(choice_code or "") == "eddie3":
        call _int_becky_talk_eddie3(girl_name)
    elif str(choice_code or "") == "eddie4":
        call _int_becky_talk_eddie4(girl_name)
    elif str(choice_code or "") == "eddie5":
        call _int_becky_talk_eddie5(girl_name)
    elif str(choice_code or "") == "eddie6":
        call _int_becky_talk_eddie6(girl_name)
    elif str(choice_code or "") == "eddie7":
        call _int_becky_talk_eddie7(girl_name)
    else:
        $ grocery_store_restore_scene_state()
        return

    call IntBeckyTalkRefresh(girl_name)
    return
