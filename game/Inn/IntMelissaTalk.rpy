label IntMelissaTalk(girl_name="melissa"):
    $ main_ui_begin_talk_state("Разговор с Мелиссой", girl_name)
    $ current_action_title = "Разговор с Мелиссой"
    $ current_action_content = None
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Мелисса вопросительно смотрит на вас, ожидая продолжения разговора."
        $ CurLocDesc = MainTxt
    call IntMelissaTalkRefresh(girl_name)
    return


label IntMelissaTalkRefresh(girl_name="melissa"):
    $ main_ui_begin_talk_state("Разговор с Мелиссой", girl_name)
    $ current_action_title = "Разговор с Мелиссой"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Function(show_girl_card_main_ui_state, girl_name)))
    if TalkedToday.get(girl_name, 0) == 0:
        $ current_action_items.append(MenuItem("Поболтать", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "talk")))
    if FlirtedToday.get(girl_name, 0) == 0 and family_social_threshold_met(girl_name, "flirt"):
        $ current_action_items.append(MenuItem("Пофлиртовать", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "flirt")))
    if GiftedToday.get(girl_name, 0) == 0 and family_social_threshold_met(girl_name, "gift"):
        $ current_action_items.append(MenuItem("Подарить что-нибудь", Function(main_ui_call_label, "PlayerCardGiftToFixedTargetMenu", girl_name)))
        if player_card_has_shareable_items() and family_social_threshold_met(girl_name, "share"):
            $ current_action_items.append(MenuItem("Поделиться угощением", Function(main_ui_call_label, "PlayerCardShareToFixedTargetMenu", girl_name)))
    if melissa_storage_thanks_available():
        $ current_action_items.append(MenuItem("Послушать, что Мелисса скажет о кладовой", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "storage_thanks")))
    if melissa_room_problem_available():
        $ current_action_items.append(MenuItem("Спросить Мелиссу о проблеме в ее комнате", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "room_problem")))
    if str(CurLoc or "") == "TavernMain" and clara_visible_in_location("TavernMain") and int(MelissaVar.get("AskedAboutClaraDay", -1) or -1) != int(dayspassed or 0) and int(AskedToday.get(girl_name, 0) or 0) == 0:
        $ current_action_items.append(MenuItem("Спросить Мелиссу о Клариссе", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "ask_clara")))
    if int(AskedToday.get(girl_name, 0) or 0) == 0 and household_special_talk_available(girl_name):
        $ _melissa_special_entry = household_special_talk_entry(girl_name)
        if _melissa_special_entry is not None:
            $ current_action_items.append(MenuItem(str(_melissa_special_entry.get("label", "Спросить о чем-то важном") or "Спросить о чем-то важном"), Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "insight")))

    if Talked.get(girl_name, 0) < 3 and Friends.get(girl_name, 0) < 5:
        $ current_action_items.append(MenuItem("Попробовать помириться с Мелиссой", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "reconcile")))

    if Friends.get(girl_name, 0) > 8 and CheckDailyEventExists("", "BuyDressTom") == 0 and CheckDailyEventExists(girl_name, "BuyDress") == 0 and Talked.get(girl_name, 0) < 2 and week != 6:
        $ current_action_items.append(MenuItem("Предложить купить Мелиссе обновку", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "buy_dress")))
    if int(AskedToday.get(girl_name, 0) or 0) == 0 and int(Friends.get(girl_name, 0) or 0) >= 15:
        $ current_action_items.append(MenuItem("Спросить, что для нее сейчас важнее всего", Function(main_ui_call_label, "IntMelissaTalkApply", girl_name, "priorities")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntMelissaTalkApply(girl_name="melissa", choice_code=""):
    if str(choice_code or "") == "inspect":
        call ShowGirlCard(girl_name)
        return

    if str(choice_code or "") == "reconcile":
        $ MainTxt = "Вы подошли к Мелиссе и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
        if renpy.random.randint(1, 3) == 1:
            $ MainTxt += "\n\nМелисса благосклонно выслушала вас, обняла, поцеловала в щечку и сказала, что очень дорожит вами и все понимает!"
            call SlutFriendsIncrease(girl_name, 6, 1, 1, 0, 0, 0)
        else:
            $ MainTxt += "\n\nМелисса холодно выслушала вас, презрительно отвернулась и пошла прочь."
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "talk":
        $ _talk_result = player_talk_to(girl_name)
        $ MainTxt = str(_talk_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "flirt":
        $ _flirt_result = player_flirt_with(girl_name)
        $ MainTxt = str(_flirt_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "buy_dress":
        call IntMelissaDressChange(girl_name)
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ask_clara":
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ MelissaVar["AskedAboutClaraDay"] = int(dayspassed or 0)
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "Вы осторожно расспрашиваете Мелиссу о Клариссе. Мелисса с улыбкой признается, что Кларисса любит заглядывать к вам не только ради болтовни, а еще потому, что у вас в трактире ей заметно свободнее дышится. «Она хорошая, просто привыкла скрывать это за светскими манерами», - тихо добавляет Мелисса."
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "storage_thanks":
        $ MelissaVar["StorageThanksDay"] = int(dayspassed or 0)
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "Мелисса сама возвращается к теме кладовой и уже без колкости благодарит вас за помощь. \"Когда знаешь, что с этой дрянью внизу не придется возиться одной, работать куда легче,\" говорит она. Потом, помедлив, добавляет, что если крысы опять полезут к мешкам, она скорее позовет вас сразу, чем будет молча злиться."
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "room_problem":
        $ MelissaVar["RoomProblemAskDay"] = int(dayspassed or 0)
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "Стоит вам спросить, как Мелисса почти сразу принимается жаловаться на свою комнату: то под потолком опять шуршат летучие мыши, то в углу висит свежая паутина, то ночью кажется, будто по балкам кто-то скребется нарочно. \"Если это снова начнется, я тебя еще попрошу помочь,\" говорит она уже вполне прямо. Похоже, теперь ей проще не копить раздражение, а сразу звать вас."
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "insight":
        $ _special_entry = household_special_talk_entry(girl_name)
        if _special_entry is None:
            call IntMelissaTalkRefresh(girl_name)
            return
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ Talked[girl_name] = int(Talked.get(girl_name, 0) or 0) + 1
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ household_advance_special_talk(girl_name)
        $ MainTxt = str(_special_entry.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "priorities":
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ Talked[girl_name] = int(Talked.get(girl_name, 0) or 0) + 1
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "Вы спрашиваете Мелиссу, что для нее сейчас важнее всего. Она на миг задумывается, потом отвечает спокойно и неожиданно открыто.\n\n\"Чтобы в доме было тише и ровнее. Чтобы можно было работать без постоянной ругани и чтобы меня не дергали по пустякам. Но еще мне важно знать, что меня здесь слушают, а не просто считают одной из рабочих рук,\" говорит Мелисса, поднимая на вас внимательный взгляд."
        $ CurLocDesc = MainTxt
        call IntMelissaTalkRefresh(girl_name)
        return

    return


label IntMelissaTalkRestore:
    $ main_ui_end_talk_state()
    return
