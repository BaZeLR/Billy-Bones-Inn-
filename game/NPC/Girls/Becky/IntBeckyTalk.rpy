# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntBeckyTalk(girl_name="becky"):
    $ _becky_name = str(girl_name or "becky").lower()
    $ Becky.update()
    if str(CurLoc or "") == "GroceryStore":
        vscene grocery_store_grocer_picture("becky")
    else:
        $ _becky_picture = str(girl_card_portrait_path(_becky_name) or "").strip()
        if str(_becky_picture or "").strip():
            vscene _becky_picture

    $ main_ui_begin_talk_state("Разговор с Бекки", _becky_name)
    $ current_action_title = "Разговор с Бекки"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items = []
    $ current_action_title = "Разговор с Бекки"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items = []
    $ current_action_title = "Разговор с Бекки"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items = []
    if str(CurLoc or "") == "GroceryStore":
        $ MainTxt = "За прилавком стоит сама Бекки Блэнкеншип. Это высокая рыжая женщина с полной грудью, ей на вид немного меньше сорока. Ее муж умер от болезни примерно за год до того, как ваш отец купил \"Дикого Жеребца\"."
        if current_game_day() > 30 and current_game_day() <= 70:
            $ MainTxt += "\n\nВы знаете, что ваша мама с ней недавно подружилась."
        elif current_game_day() > 70:
            $ MainTxt += "\n\nОна с вашей мамой - лучшие подруги."
        $ CurLocDesc = MainTxt
    elif str(MainTxt or "").strip() == "":
        $ MainTxt = "Бекки внимательно смотрит на вас, ожидая, что вы захотите обсудить."
        $ CurLocDesc = MainTxt

    $ initStoryEventRuntime(True)
    $ current_action_items.append(MenuItem("Осмотреть", Function(NpcActionLookState, _becky_name, CurLoc)))
    $ current_action_items.append(MenuItem("Поболтать со вдовой Блэнкеншип о разной фигне", Call("_int_becky_talk_smalltalk", _becky_name)))

    if Becky.rel >= 3:
        $ current_action_items.append(MenuItem("Поболтать с Бекки о более личных вещах", Call("_int_becky_talk_personal", _becky_name)))

    if becky_dress_change_has_options(_becky_name):
        $ current_action_items.append(MenuItem("Поговорить с Бекки об одежде", Call("IntBeckyDressChange", _becky_name)))

    if story_event_available("talk_becky", "becky_talk_inga1"):
        $ current_action_items.append(MenuItem("Спросить Бекки про дочку с женихом", Call("checkTriggers", "talk_becky", "becky_talk_inga1", 0)))
    if story_event_available("talk_becky", "becky_talk_inga2"):
        $ current_action_items.append(MenuItem("Распросить еще про дочку", Call("checkTriggers", "talk_becky", "becky_talk_inga2", 0)))
    if story_event_available("talk_becky", "becky_talk_lucas"):
        $ current_action_items.append(MenuItem("Распросить про Лукаса, жениха Ингенборг", Call("checkTriggers", "talk_becky", "becky_talk_lucas", 0)))

    if story_event_available("talk_becky", "becky_talk_husband1"):
        $ current_action_items.append(MenuItem("Распросить Бекки про ее покойного мужа", Call("checkTriggers", "talk_becky", "becky_talk_husband1", 0)))
    if story_event_available("talk_becky", "becky_talk_husband2"):
        $ current_action_items.append(MenuItem("Распросить еще про Эрика", Call("checkTriggers", "talk_becky", "becky_talk_husband2", 0)))
    if story_event_available("talk_becky", "becky_talk_husband3"):
        $ current_action_items.append(MenuItem("Узнать что сталось с другими подружками Эрика", Call("checkTriggers", "talk_becky", "becky_talk_husband3", 0)))
    if story_event_available("talk_becky", "becky_talk_husband4"):
        $ current_action_items.append(MenuItem("Спросить про остальных подружек Эрика", Call("checkTriggers", "talk_becky", "becky_talk_husband4", 0)))

    if story_event_available("talk_becky", "becky_talk_eddie1"):
        $ current_action_items.append(MenuItem("Спросить про Эдди, управляющего лавкой", Call("checkTriggers", "talk_becky", "becky_talk_eddie1", 0)))
    if story_event_available("talk_becky", "becky_talk_eddie2"):
        $ current_action_items.append(MenuItem("Рассказать про игру Эдди и Жоржетты", Call("checkTriggers", "talk_becky", "becky_talk_eddie2", 0)))

    if story_event_available("talk_becky", "becky_talk_invite"):
        $ current_action_items.append(MenuItem("Попробовать напросится в гости", Call("checkTriggers", "talk_becky", "becky_talk_invite", 0)))
    if story_event_available("talk_becky", "becky_talk_lastvisit"):
        $ current_action_items.append(MenuItem("Спросить о прошлом визите в гости", Call("checkTriggers", "talk_becky", "becky_talk_lastvisit", 0)))

    if story_event_available("talk_becky", "becky_talk_eddie3"):
        $ current_action_items.append(MenuItem("Указать Бекки на поведение ее управляющего", Call("checkTriggers", "talk_becky", "becky_talk_eddie3", 0)))
    if story_event_available("talk_becky", "becky_talk_eddie4"):
        $ current_action_items.append(MenuItem("Рассказать что Эдди требует, чтобы Жоржетта изображала Бекки", Call("checkTriggers", "talk_becky", "becky_talk_eddie4", 0)))
    if story_event_available("talk_becky", "becky_talk_eddie5"):
        $ current_action_items.append(MenuItem("Возмутиться поведением Эдди", Call("checkTriggers", "talk_becky", "becky_talk_eddie5", 0)))
    if story_event_available("talk_becky", "becky_talk_eddie6"):
        $ current_action_items.append(MenuItem("Посоветовать Бекки быть повнимательнее к нуждам Эдди", Call("checkTriggers", "talk_becky", "becky_talk_eddie6", 0)))
    if story_event_available("talk_becky", "becky_talk_eddie7"):
        $ current_action_items.append(MenuItem("Поговорить с Бекки об Эдди", Call("checkTriggers", "talk_becky", "becky_talk_eddie7", 0)))

    if story_event_available("talk_becky", "becky_talk_pregnancy"):
        $ current_action_items.append(MenuItem("Спросить, знает ли она от кого затяжелела", Call("checkTriggers", "talk_becky", "becky_talk_pregnancy", 0)))

    if story_event_available("talk_becky", "becky_talk_sherwood_offer"):
        $ current_action_items.append(MenuItem("Насчет твоего предложения, в чем там все-таки дело?", Call("checkTriggers", "talk_becky", "becky_talk_sherwood_offer", 0)))
    if story_event_available("talk_becky", "becky_talk_sherwood_elves"):
        $ current_action_items.append(MenuItem("А чего ты сама с эльфами не торгуешь?", Call("checkTriggers", "talk_becky", "becky_talk_sherwood_elves", 0)))
    if story_event_available("talk_becky", "becky_talk_sherwood_fingal"):
        $ current_action_items.append(MenuItem("А твое предложеньице с фингалом у твоего сынка не связанно, случаем?", Call("checkTriggers", "talk_becky", "becky_talk_sherwood_fingal", 0)))
    if story_event_available("talk_becky", "becky_talk_sherwood_warn"):
        $ current_action_items.append(MenuItem("О какой-такой загвоздке ты говорила?", Call("checkTriggers", "talk_becky", "becky_talk_sherwood_warn", 0)))
    if story_event_available("talk_becky", "becky_talk_sherwood_road"):
        $ current_action_items.append(MenuItem("Насчет дороги в Куниделл", Call("checkTriggers", "talk_becky", "becky_talk_sherwood_road", 0)))
    if story_event_available("talk_becky", "becky_talk_sherwood_lied"):
        $ current_action_items.append(MenuItem("Так что же ты меня дурила-то?", Call("checkTriggers", "talk_becky", "becky_talk_sherwood_lied", 0)))
    if story_event_available("talk_becky", "becky_talk_sherwood_robbed"):
        $ current_action_items.append(MenuItem("Меня ограбили!!!", Call("checkTriggers", "talk_becky", "becky_talk_sherwood_robbed", 0)))
    if story_event_available("talk_becky", "becky_talk_sherwood_howto"):
        $ current_action_items.append(MenuItem("Так как мне в Куниделл попасть-то?", Call("checkTriggers", "talk_becky", "becky_talk_sherwood_howto", 0)))
    if story_event_available("talk_becky", "becky_talk_sherwood_warned"):
        $ current_action_items.append(MenuItem("Так что ж ты меня не предупредила-то?", Call("checkTriggers", "talk_becky", "becky_talk_sherwood_warned", 0)))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return
