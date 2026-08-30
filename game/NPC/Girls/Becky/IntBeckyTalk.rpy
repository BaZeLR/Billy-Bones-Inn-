# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntBeckyTalk(girl_name="becky"):
    $ renpy.dynamic("_becky_name", "_becky_picture", "_grocery_breastfeeding_text", "_grocery_kids_text")
    $ _becky_name = str(girl_name or "becky").lower()
    $ Becky.update()
    $ main_ui_begin_talk_state("Разговор с Бекки", _becky_name)
    if str(rooms.current_code or "") == "GroceryStore":
        vscene grocery_store_grocer_picture("becky")
    else:
        $ _becky_picture = str(girl_card_portrait_path(_becky_name) or "").strip()
        if str(_becky_picture or "").strip():
            vscene _becky_picture
    if str(rooms.current_code or "") == "GroceryStore":
        $ scene_runtime.text = "За прилавком стоит сама Бекки Блэнкеншип. Это высокая рыжая женщина с полной грудью, ей на вид немного меньше сорока. Ее муж умер от болезни примерно за год до того, как ваш отец купил \"Дикого Жеребца\"."
        if current_game_day() > 30 and current_game_day() <= 70:
            $ scene_runtime.text += "\n\nВы знаете, что ваша мама с ней недавно подружилась."
        elif current_game_day() > 70:
            $ scene_runtime.text += "\n\nОна с вашей мамой - лучшие подруги."
        $ _grocery_breastfeeding_text = DescribeBreastFeeding("becky", 3)
        $ _grocery_kids_text = ShowFullKidsListByAge("becky", "inga")
        if _grocery_breastfeeding_text:
            $ scene_runtime.text += "\n\n" + _grocery_breastfeeding_text
        if _grocery_kids_text:
            $ scene_runtime.text += "\n\n" + _grocery_kids_text
        $ scene_runtime.location_text = scene_runtime.text
    elif str(scene_runtime.text or "").strip() == "":
        $ scene_runtime.text = "Бекки внимательно смотрит на вас, ожидая, что вы захотите обсудить."
        $ scene_runtime.location_text = scene_runtime.text

    while str(main_ui_runtime.mode or "") == "talk":
        $ initStoryEventRuntime(True)
        menu:
            "Осмотреть":
                call ShowGirlCard(_becky_name)
            "Поболтать со вдовой Блэнкеншип о разной фигне":
                call _int_becky_talk_smalltalk(_becky_name)
            "Поболтать с Бекки о более личных вещах" if Becky.rel >= 3:
                call _int_becky_talk_personal(_becky_name)
            "Поговорить с Бекки об одежде" if Becky.dress_change_has_options(_becky_name):
                call IntBeckyDressChange(_becky_name)
            "Спросить Бекки про дочку с женихом" if story_event_available("talk_becky", "becky_talk_inga1"):
                call checkTriggers("talk_becky", "becky_talk_inga1", 0)
            "Распросить еще про дочку" if story_event_available("talk_becky", "becky_talk_inga2"):
                call checkTriggers("talk_becky", "becky_talk_inga2", 0)
            "Распросить про Лукаса, жениха Ингенборг" if story_event_available("talk_becky", "becky_talk_lucas"):
                call checkTriggers("talk_becky", "becky_talk_lucas", 0)
            "Распросить Бекки про ее покойного мужа" if story_event_available("talk_becky", "becky_talk_husband1"):
                call checkTriggers("talk_becky", "becky_talk_husband1", 0)
            "Распросить еще про Эрика" if story_event_available("talk_becky", "becky_talk_husband2"):
                call checkTriggers("talk_becky", "becky_talk_husband2", 0)
            "Узнать что сталось с другими подружками Эрика" if story_event_available("talk_becky", "becky_talk_husband3"):
                call checkTriggers("talk_becky", "becky_talk_husband3", 0)
            "Спросить про остальных подружек Эрика" if story_event_available("talk_becky", "becky_talk_husband4"):
                call checkTriggers("talk_becky", "becky_talk_husband4", 0)
            "Спросить про Эдди, управляющего лавкой" if story_event_available("talk_becky", "becky_talk_eddie1"):
                call checkTriggers("talk_becky", "becky_talk_eddie1", 0)
            "Рассказать про игру Эдди и Жоржетты" if story_event_available("talk_becky", "becky_talk_eddie2"):
                call checkTriggers("talk_becky", "becky_talk_eddie2", 0)
            "Попробовать напросится в гости" if Becky.home_visit_stage == 2 and Becky.rel > 12 and Becky.talk_count() < 2:
                call story_becky_home_invite_talk_0(_becky_name)
            "Спросить о прошлом визите в гости" if Becky.home_visit_count > 0 and Becky.talk_count() < 2:
                call story_becky_home_last_visit_talk_0(_becky_name)
            "Указать Бекки на поведение ее управляющего" if Becky.home_visit_stage >= 3 and (Eddie.saw_mother_sex or Becky.home_sex_unlocked) and Becky.home_visit_stage < 7 and Becky.eddie_join_stage < 4 and Becky.talk_count() < 2:
                call story_becky_talk_eddie_behavior_0(_becky_name)
            "Рассказать что Эдди требует, чтобы Жоржетта изображала Бекки" if Becky.eddie_georgett_stage > 1 and Becky.home_visit_stage < 7 and Becky.talk_count() < 2:
                call story_becky_talk_eddie_georgett_1(_becky_name)
            "Возмутиться поведением Эдди" if Becky.georgett_mentioned and Becky.home_visit_stage < 7 and Becky.talk_count() < 2:
                call story_becky_talk_eddie_reaction_0(_becky_name)
            "Посоветовать Бекки быть повнимательнее к нуждам Эдди" if Becky.georgett_mentioned and Becky.home_visit_stage < 7 and Becky.talk_count() < 2:
                call story_becky_talk_eddie_reaction_1(_becky_name)
            "Поговорить с Бекки об Эдди" if ((Becky.eddie_join_stage == 4 and Becky.asked_about_eddie_sex_stage == 0) or (Becky.home_visit_stage >= 7 and Becky.asked_about_eddie_sex_stage < 2)) and Becky.talk_count() < 2:
                call story_becky_talk_eddie_after_sex_0(_becky_name)
            "Спросить, знает ли она от кого затяжелела" if Becky.talk_count() < 2 and Becky.rel >= 8 and int(Becky.stats.get("pregnancy", 0) or 0) >= 120 and str(DaddyAskBuildPhrase(_becky_name) or "") != "":
                call story_becky_talk_pregnancy_0(_becky_name)
            "Насчет твоего предложения, в чем там все-таки дело?" if Becky.talk_count() < 2 and Becky.trade_offer_stage == 2:
                call story_becky_sherwood_offer_0(_becky_name)
            "А чего ты сама с эльфами не торгуешь?" if Becky.talk_count() < 2 and Becky.trade_offer_stage == 1 and not Becky.asked_about_elf_trade:
                call story_becky_sherwood_elves_0(_becky_name)
            "А твое предложеньице с фингалом у твоего сынка не связанно, случаем?" if Becky.trade_offer_stage == 1 and Eddie.fingal_talk_stage > 0 and not Becky.fingal_connection_clarified and Becky.admitted_sherwood_stage == 0:
                call story_becky_sherwood_fingal_0(_becky_name)
            "О какой-такой загвоздке ты говорила?" if Becky.trade_offer_stage == 1 and Becky.sherwood_warning_stage == 1 and Becky.admitted_sherwood_stage == 0:
                call story_becky_sherwood_warn_0(_becky_name)
            "Насчет дороги в Куниделл" if Becky.talk_count() < 2 and Becky.trade_offer_stage == 1 and Becky.admitted_sherwood_stage == 0 and Becky.knows_blackwood:
                call story_becky_sherwood_road_0(_becky_name)
            "Так что же ты меня дурила-то?" if Becky.trade_offer_stage == 1 and Becky.admitted_sherwood_stage == 1:
                call story_becky_sherwood_lied_0(_becky_name)
            "Меня ограбили!!!" if Becky.talk_count() < 2 and Becky.robin_robbery_stage == 1:
                call story_becky_sherwood_robbed_0(_becky_name)
            "Так как мне в Куниделл попасть-то?" if Becky.talk_count() < 2 and Becky.robbery_consolation_count == 0 and Becky.robin_robbery_stage >= 2:
                call story_becky_sherwood_howto_0(_becky_name)
            "Так что ж ты меня не предупредила-то?" if Becky.robin_robbery_stage == 2 and Becky.admitted_sherwood_stage == 0:
                call story_becky_sherwood_warned_0(_becky_name)
            "Закончить разговор":
                $ main_ui_end_talk_state()
                return

    return
