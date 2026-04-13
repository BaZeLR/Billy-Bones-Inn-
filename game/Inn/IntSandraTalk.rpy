label IntSandraTalk(girl_name="sandra"):
    $ main_ui_begin_talk_state("Разговор с Сандрой", girl_name)
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Сандра внимательно смотрит на вас, ожидая, что вы скажете."
        $ CurLocDesc = MainTxt
    call IntSandraTalkRefresh(girl_name)
    return


label IntSandraTalkRefresh(girl_name="sandra"):
    $ main_ui_begin_talk_state("Разговор с Сандрой", girl_name)
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Function(show_girl_card_main_ui_state, girl_name)))
    if TalkedToday.get(girl_name, 0) == 0:
        $ current_action_items.append(MenuItem("Поболтать", Function(main_ui_call_label, "IntSandraTalkApply", girl_name, "talk")))
    if FlirtedToday.get(girl_name, 0) == 0 and family_social_threshold_met(girl_name, "flirt"):
        $ current_action_items.append(MenuItem("Пофлиртовать", Function(main_ui_call_label, "IntSandraTalkApply", girl_name, "flirt")))
    if GiftedToday.get(girl_name, 0) == 0 and family_social_threshold_met(girl_name, "gift"):
        $ current_action_items.append(MenuItem("Подарить что-нибудь", Function(main_ui_call_label, "PlayerCardGiftToFixedTargetMenu", girl_name)))
        if player_card_has_shareable_items() and family_social_threshold_met(girl_name, "share"):
            $ current_action_items.append(MenuItem("Поделиться угощением", Function(main_ui_call_label, "PlayerCardShareToFixedTargetMenu", girl_name)))

    if Talked.get(girl_name, 0) < 3 and Friends.get(girl_name, 0) < 5:
        $ current_action_items.append(MenuItem("Попробовать помириться с Сандрой", Function(main_ui_call_label, "IntSandraTalkApply", girl_name, "reconcile")))

    if sandra_dress_change_can_buy(girl_name):
        $ current_action_items.append(MenuItem("Предложить купить Сандре обновку", Function(main_ui_call_label, "IntSandraTalkApply", girl_name, "buy_dress")))
    if AskedToday.get(girl_name, 0) == 0 and household_special_talk_available(girl_name):
        $ _sandra_special_entry = household_special_talk_entry(girl_name)
        if _sandra_special_entry is not None:
            $ current_action_items.append(MenuItem(str(_sandra_special_entry.get("label", "Спросить о чем-то важном") or "Спросить о чем-то важном"), Function(main_ui_call_label, "IntSandraTalkApply", girl_name, "insight")))
    if AskedToday.get(girl_name, 0) == 0 and int(Friends.get(girl_name, 0) or 0) >= 15:
        $ current_action_items.append(MenuItem("Спросить, что для нее сейчас важнее всего по хозяйству", Function(main_ui_call_label, "IntSandraTalkApply", girl_name, "priorities")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntSandraTalkApply(girl_name="sandra", choice_code=""):
    if str(choice_code or "") == "inspect":
        call ShowGirlCard(girl_name)
        return

    if str(choice_code or "") == "reconcile":
        $ MainTxt = "Вы подошли к Сандре и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
        if renpy.random.randint(1, 2) == 1:
            $ MainTxt += "\n\nСандра благосклонно выслушала вас, обняла и сказала, что все еще очень привязана к вам, несмотря ни на что!"
            call SlutFriendsIncrease(girl_name, 6, 1, 1, 0, 0, 0)
        else:
            $ MainTxt += "\n\nСандра холодно выслушала вас, отвернулась и пошла прочь, не говоря ни слова."
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntSandraTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "talk":
        $ _talk_result = player_talk_to(girl_name)
        $ MainTxt = str(_talk_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntSandraTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "flirt":
        $ _flirt_result = player_flirt_with(girl_name)
        $ MainTxt = str(_flirt_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntSandraTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "buy_dress":
        call IntSandraDressChangeApply(girl_name, "buy_dress")
        return

    if str(choice_code or "") == "insight":
        $ _special_entry = household_special_talk_entry(girl_name)
        if _special_entry is None:
            call IntSandraTalkRefresh(girl_name)
            return
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ Talked[girl_name] = int(Talked.get(girl_name, 0) or 0) + 1
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ household_advance_special_talk(girl_name)
        $ MainTxt = str(_special_entry.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntSandraTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "priorities":
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ Talked[girl_name] = int(Talked.get(girl_name, 0) or 0) + 1
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "Вы прямо спрашиваете Сандру, что для нее сейчас важнее всего в доме. Сандра не сразу отвечает, потом складывает руки на груди и говорит уже без обычного раздражения.\n\n\"Чтобы в трактире был порядок, утром люди не шарахались голодными по углам, а работа шла без лишней дури. Если домочадцы сыты, умыты и знают свое дело, дальше уже и с гостями проще. А еще мне важно, чтобы ты не забывал: хозяйство держится не на одних приказах, а на том, что люди видят в тебе хозяина, который умеет думать наперед.\""
        $ CurLocDesc = MainTxt
        call IntSandraTalkRefresh(girl_name)
        return

    return


label IntSandraTalkRestore:
    $ main_ui_end_talk_state()
    return
