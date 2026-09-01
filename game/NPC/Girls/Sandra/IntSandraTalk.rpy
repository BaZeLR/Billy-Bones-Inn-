# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntSandraTalk(girl_name="sandra"):
    $ renpy.dynamic("_sandra_special_entry", "_sandra_repeat_menu")
    $ main_ui_begin_talk_state("Разговор с Сандрой", girl_name)
    $ main_ui_runtime.action_title = "Разговор с Сандрой"
    $ main_ui_runtime.action_content = None
    if str(scene_runtime.text or "").strip() == "":
        $ scene_runtime.text = "Сандра внимательно смотрит на вас, ожидая, что вы скажете."
        $ scene_runtime.location_text = scene_runtime.text
    $ _sandra_special_entry = household_special_talk_entry(girl_name) if int(Sandra.asked_today or 0) == 0 and household_special_talk_available(girl_name) else None
    $ _sandra_repeat_menu = True
    while _sandra_repeat_menu:
        $ _sandra_repeat_menu = False
        menu:
            "Осмотреть":
                call ShowGirlCard(girl_name)
            "Поговорить" if social_has_visible_topics(girl_name, "talk"):
                call SocialTalkTopicMenu(girl_name, "talk")
                $ _sandra_repeat_menu = True
            "Подарить маленький подарок" if social_interaction_allowed_for_npc(girl_name, "gift"):
                call PlayerCardGiftToFixedTargetMenu(girl_name)
                $ _sandra_repeat_menu = True
            "Попробовать помириться с мамой" if int(Sandra.talked_today or 0) < 3 and int(Sandra.rel or 0) < 5:
                call IntSandraReconcile(girl_name)
            "Предложить купить мамуле обновку" if sandra_dress_change_can_buy(girl_name):
                call IntSandraOfferBuyDress(girl_name)
            "[_sandra_special_entry.get('label', 'Спросить о чем-то важном')]" if _sandra_special_entry is not None:
                call IntSandraHouseholdInsight(girl_name)
            "Спросить, что для нее сейчас важнее всего по хозяйству" if int(Sandra.asked_today or 0) == 0 and int(Sandra.rel or 0) >= 15:
                call IntSandraHouseholdPriorities(girl_name)
            "Заняться сексом с Сандрой" if threads["sandraWeeklyEvaluation"].completed and str(rooms.current_code or "") == "TavernSandraRoom":
                call HouseholdSexEngine(girl_name, rooms.current_code, "sex")
            "Попросить Сандру помочь рукой" if threads["sandraWeeklyEvaluation"].completed and str(rooms.current_code or "") == "TavernSandraRoom" and player.intimacy.can_cum():
                call HouseholdSexEngine(girl_name, rooms.current_code, "handjob")
            "Попросить Сандру сделать минет" if threads["sandraWeeklyEvaluation"].completed and str(rooms.current_code or "") == "TavernSandraRoom" and player.intimacy.can_cum():
                call HouseholdSexEngine(girl_name, rooms.current_code, "blowjob")
            "Назад":
                $ main_ui_end_talk_state()
                return
    return


label IntSandraReconcile(girl_name="sandra"):
    $ scene_runtime.text = "Вы подошли к Сандре и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и вы все должны дружно работать вместе, чтобы преуспеть."
    if procedural_randint(1, 2, key="procedural:NPC/Girls/Sandra/IntSandraTalk.rpy:procedural_randint:40:1") == 1:
        $ scene_runtime.text += "\n\nСандра благосклонно выслушала вас, обняла и сказала, что она всегда будет вас любить, несмотря ни на что!"
        call SlutFriendsIncrease(girl_name, 6, 1, 1, 0, 0, 0)
    else:
        $ scene_runtime.text += "\n\nСандра холодно выслушала вас, отвернулась и пошла прочь, не говоря ни слова."
    $ Sandra.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Разговор с Сандрой"
    $ main_ui_runtime.action_content = None
    return


label IntSandraHouseholdInsight(girl_name="sandra"):
    $ renpy.dynamic("_special_entry")
    $ _special_entry = household_special_talk_entry(girl_name)
    if _special_entry is None:
        $ scene_runtime.text = "Сейчас Сандра не готова говорить о хозяйстве подробнее."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = "Разговор с Сандрой"
        $ main_ui_runtime.action_content = None
        return
    $ Sandra.mark_asked()
    $ Sandra.mark_talked()
    $ Sandra.change_social(friend_delta=1, open_delta=1)
    $ household_advance_special_talk(girl_name)
    $ scene_runtime.text = str(_special_entry.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Разговор с Сандрой"
    $ main_ui_runtime.action_content = None
    return


label IntSandraHouseholdPriorities(girl_name="sandra"):
    $ Sandra.mark_asked()
    $ Sandra.mark_talked()
    $ Sandra.change_social(friend_delta=1, open_delta=1)
    $ scene_runtime.text = "Вы прямо спрашиваете Сандру, что для нее сейчас важнее всего в доме. Сандра не сразу отвечает, потом складывает руки на груди и говорит уже без обычного раздражения.\n\n\"Чтобы в трактире был порядок, утром люди не шарахались голодными по углам, а работа шла без лишней дури. Если домочадцы сыты, умыты и знают свое дело, дальше уже и с гостями проще. А еще мне важно, чтобы ты не забывал: хозяйство держится не на одних приказах, а на том, что люди видят в тебе хозяина, который умеет думать наперед.\""
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Разговор с Сандрой"
    $ main_ui_runtime.action_content = None
    return
