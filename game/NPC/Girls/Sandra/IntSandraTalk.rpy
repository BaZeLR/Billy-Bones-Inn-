        "Извиниться перед Сандрой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntSandraTalk        "Извиниться перед Сандрой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntSandraTalk        "Извиниться перед Сандрой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntSandraTalk        "Извиниться перед Сандрой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntSandraTalk        "Извиниться перед Сандрой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntSandraTalk        "Извиниться перед Сандрой" if talk_system_apology_available(girl_name):
            call TalkSystemApology(girl_name)
            jump IntSandraTalk# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntSandraTalk(girl_name="sandra"):
    $ main_ui_begin_talk_state("Разговор с Сандрой", girl_name)
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    if not getPersonInfo(girl_name).social_action_allowed("talk"):
        $ MainTxt = "Сандра отвечает коротко и по делу. Сейчас между вами еще нет того доверия, которое позволило бы говорить с ней не только о работе."
        $ CurLocDesc = MainTxt
        menu:
            "Назад":
                $ main_ui_end_talk_state()
                $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    return
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Сандра внимательно смотрит на вас, ожидая, что вы скажете."
        $ CurLocDesc = MainTxt
    $ _sandra_special_entry = household_special_talk_entry(girl_name) if int(Sandra.asked_today or 0) == 0 and household_special_talk_available(girl_name) else None
    menu:
            "Осмотреть":
                call ShowGirlCard(girl_name)
            "Поговорить" if old_point_smalltalk_available(girl_name):
                call OldPointSmallTalkMenu(girl_name)
            "Флиртовать" if old_point_action_unlocked(girl_name, "flirt"):
                call OldPointFlirtAttempt(girl_name)
            "Подарить маленький подарок" if old_point_action_unlocked(girl_name, "gift"):
                call PlayerCardGiftToFixedTargetMenu(girl_name)
            "Коснуться ее смелее" if old_point_action_unlocked(girl_name, "kino"):
                call OldPointKinoAttempt(girl_name)
            "Извиниться перед Сандрой" if old_point_apology_available(girl_name):
                call OldPointApology(girl_name)
            "Предложить купить Сандре обновку" if sandra_dress_change_can_buy(girl_name):
                call IntSandraOfferBuyDress(girl_name)
            "[_sandra_special_entry.get('label', 'Спросить о чем-то важном')]" if _sandra_special_entry is not None:
                call IntSandraHouseholdInsight(girl_name)
            "Спросить, что для нее сейчас важнее всего по хозяйству" if int(Sandra.asked_today or 0) == 0 and int(Sandra.rel or 0) >= 15:
                call IntSandraHouseholdPriorities(girl_name)
            "Уединиться с Сандрой" if Sandra.sex_available() and str(CurLoc or "") == "TavernSandraRoom":
                call SandraSexEngine(girl_name, CurLoc)
            "Назад":
                $ main_ui_end_talk_state()
                $ current_action_items = [
            MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
            MenuItem("Назад", Function(main_ui_end_talk_state)),
        ]
        $ current_action_items = [
            MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
            MenuItem("Назад", Function(main_ui_end_talk_state)),
        ]
        $ current_action_items = [
            MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
            MenuItem("Назад", Function(main_ui_end_talk_state)),
        ]
        return
label IntSandraReconcile(girl_name="sandra"):
    $ MainTxt = "Вы подошли к Сандре и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
    if procedural_randint(1, 2, key="procedural:NPC/Girls/Sandra/IntSandraTalk.rpy:procedural_randint:40:1") == 1:
        $ MainTxt += "\n\nСандра благосклонно выслушала вас, обняла и сказала, что все еще очень привязана к вам, несмотря ни на что!"
        call SlutFriendsIncrease(girl_name, 6, 1, 1, 0, 0, 0)
    else:
        $ MainTxt += "\n\nСандра холодно выслушала вас, отвернулась и пошла прочь, не говоря ни слова."
    $ Sandra.mark_talked()
    $ CurLocDesc = MainTxt
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    return


label IntSandraHouseholdInsight(girl_name="sandra"):
    $ _special_entry = household_special_talk_entry(girl_name)
    if _special_entry is None:
        $ MainTxt = "Сейчас Сандра не готова говорить о хозяйстве подробнее."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Разговор с Сандрой"
        $ current_action_content = None
        $ current_action_items = [
            MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
            MenuItem("Назад", Function(main_ui_end_talk_state)),
        ]
        $ current_action_title = "Разговор с Сандрой"
        $ current_action_content = None
        return
    $ Sandra.mark_asked()
    $ Sandra.mark_talked()
    $ Sandra.change_social(friend_delta=1, open_delta=1)
    $ household_advance_special_talk(girl_name)
    $ MainTxt = str(_special_entry.get("text", "") or "")
    $ CurLocDesc = MainTxt
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    return


label IntSandraHouseholdPriorities(girl_name="sandra"):
    $ Sandra.mark_asked()
    $ Sandra.mark_talked()
    $ Sandra.change_social(friend_delta=1, open_delta=1)
    $ MainTxt = "Вы прямо спрашиваете Сандру, что для нее сейчас важнее всего в доме. Сандра не сразу отвечает, потом складывает руки на груди и говорит уже без обычного раздражения.\n\n\"Чтобы в трактире был порядок, утром люди не шарахались голодными по углам, а работа шла без лишней дури. Если домочадцы сыты, умыты и знают свое дело, дальше уже и с гостями проще. А еще мне важно, чтобы ты не забывал: хозяйство держится не на одних приказах, а на том, что люди видят в тебе хозяина, который умеет думать наперед.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Вернуться к разговору", Call("IntSandraTalk", girl_name)),
        MenuItem("Назад", Function(main_ui_end_talk_state)),
    ]
    $ current_action_title = "Разговор с Сандрой"
    $ current_action_content = None
    return
