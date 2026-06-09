# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntSandraTalk(girl_name="sandra"):
    $ main_ui_begin_talk_state("Разговор с Сандрой", girl_name)
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Function(NpcActionLookState, girl_name, CurLoc)))
    if not getPersonInfo(girl_name).social_action_allowed("talk"):
        $ MainTxt = "Сандра отвечает коротко и по делу. Сейчас между вами еще нет того доверия, которое позволило бы говорить с ней не только о работе."
        $ CurLocDesc = MainTxt
        $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
        return
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Сандра внимательно смотрит на вас, ожидая, что вы скажете."
        $ CurLocDesc = MainTxt
    $ current_action_items.extend(social_core_action_items(girl_name, "IntSandraTalk"))

    if Talked.get(girl_name, 0) < 3 and Friends.get(girl_name, 0) < 5:
        $ current_action_items.append(MenuItem("Попробовать помириться с Сандрой", Function(main_ui_call_label, "IntSandraReconcile", girl_name)))

    if sandra_dress_change_can_buy(girl_name):
        $ current_action_items.append(MenuItem("Предложить купить Сандре обновку", Function(main_ui_call_label, "IntSandraOfferBuyDress", girl_name)))
    if AskedToday.get(girl_name, 0) == 0 and household_special_talk_available(girl_name):
        $ _sandra_special_entry = household_special_talk_entry(girl_name)
        if _sandra_special_entry is not None:
            $ current_action_items.append(MenuItem(str(_sandra_special_entry.get("label", "Спросить о чем-то важном") or "Спросить о чем-то важном"), Function(main_ui_call_label, "IntSandraHouseholdInsight", girl_name)))
    if AskedToday.get(girl_name, 0) == 0 and int(Friends.get(girl_name, 0) or 0) >= 15:
        $ current_action_items.append(MenuItem("Спросить, что для нее сейчас важнее всего по хозяйству", Function(main_ui_call_label, "IntSandraHouseholdPriorities", girl_name)))
    if Sandra.sex_available() and str(CurLoc or "") == "TavernSandraRoom":
        $ current_action_items.append(MenuItem("Уединиться с Сандрой", Function(main_ui_call_label, "SandraSexEngine", girl_name, CurLoc)))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntSandraReconcile(girl_name="sandra"):
    $ MainTxt = "Вы подошли к Сандре и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
    if renpy.random.randint(1, 2) == 1:
        $ MainTxt += "\n\nСандра благосклонно выслушала вас, обняла и сказала, что все еще очень привязана к вам, несмотря ни на что!"
        call SlutFriendsIncrease(girl_name, 6, 1, 1, 0, 0, 0)
    else:
        $ MainTxt += "\n\nСандра холодно выслушала вас, отвернулась и пошла прочь, не говоря ни слова."
    $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
    $ CurLocDesc = MainTxt
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Function(main_ui_call_label, "IntSandraTalk", girl_name)),
        MenuItem("Закончить разговор", Function(main_ui_end_talk_state)),
    ]
    return


label IntSandraHouseholdInsight(girl_name="sandra"):
    $ _special_entry = household_special_talk_entry(girl_name)
    if _special_entry is None:
        $ MainTxt = "Сейчас Сандра не готова говорить о хозяйстве подробнее."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Разговор с Сандрой"
        $ current_action_content = None
        $ current_action_items = [
            MenuItem("Вернуться к разговору", Function(main_ui_call_label, "IntSandraTalk", girl_name)),
            MenuItem("Закончить разговор", Function(main_ui_end_talk_state)),
        ]
        return
    $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
    $ Talked[girl_name] = int(Talked.get(girl_name, 0) or 0) + 1
    $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
    $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
    $ household_advance_special_talk(girl_name)
    $ MainTxt = str(_special_entry.get("text", "") or "")
    $ CurLocDesc = MainTxt
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Function(main_ui_call_label, "IntSandraTalk", girl_name)),
        MenuItem("Закончить разговор", Function(main_ui_end_talk_state)),
    ]
    return


label IntSandraHouseholdPriorities(girl_name="sandra"):
    $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
    $ Talked[girl_name] = int(Talked.get(girl_name, 0) or 0) + 1
    $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
    $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
    $ MainTxt = "Вы прямо спрашиваете Сандру, что для нее сейчас важнее всего в доме. Сандра не сразу отвечает, потом складывает руки на груди и говорит уже без обычного раздражения.\n\n\"Чтобы в трактире был порядок, утром люди не шарахались голодными по углам, а работа шла без лишней дури. Если домочадцы сыты, умыты и знают свое дело, дальше уже и с гостями проще. А еще мне важно, чтобы ты не забывал: хозяйство держится не на одних приказах, а на том, что люди видят в тебе хозяина, который умеет думать наперед.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Function(main_ui_call_label, "IntSandraTalk", girl_name)),
        MenuItem("Закончить разговор", Function(main_ui_end_talk_state)),
    ]
    return
