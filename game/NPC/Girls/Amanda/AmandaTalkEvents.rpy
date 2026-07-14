# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def amanda_talk_work_tip_ready():
        return (
            int(Amanda.rel or 0) >= 5
            and int(Amanda.asked_today or 0) == 0
            and int(Amanda.var_int("talk_work_tip_day", -1) or -1) != int(current_game_day() or 0)
        )

    def amanda_talk_look_opinion_ready():
        return (
            int(Amanda.rel or 0) >= 10
            and int(Amanda.corruption or 0) >= 5
            and int(Amanda.asked_today or 0) == 0
            and int(Amanda.var_int("talk_look_opinion_day", -1) or -1) != int(current_game_day() or 0)
        )


label AmandaTalkWorkTipEvent(girl_name="amanda"):
    $ Amanda.mark_asked()
    $ Amanda.mark_talked()
    $ Amanda.set_var_int("talk_work_tip_day", int(current_game_day() or 0))
    $ Amanda.change_social(friend_delta=1)
    $ calendar_v2.advance_minutes(10)
    vscene "images/amanda/tavern/waitress1.jpeg"
    $ MainTxt = "Вы спрашиваете Аманду, что сейчас сильнее всего влияет на настроение девочек в трактире.\n\nАманда сперва фыркает, будто ответ очевиден, потом все же говорит тише: \"Когда в доме есть нормальная еда, мед к чаю и мясо после охоты, все становятся мягче. Даже Сандра меньше пилит. А если еще дать девочке почувствовать, что она не просто служанка с подносом, а красивая часть дома, тогда она сама начинает стараться.\""
    $ CurLocDesc = MainTxt
    return


label AmandaTalkLookOpinionEvent(girl_name="amanda"):
    $ Amanda.mark_asked()
    $ Amanda.mark_talked()
    $ Amanda.set_var_int("talk_look_opinion_day", int(current_game_day() or 0))
    $ calendar_v2.advance_minutes(10)
    vscene "images/amanda/tavern/waitress3.jpeg"
    $ MainTxt = "Аманда задерживается рядом после обычных слов и неожиданно расправляет платье на бедрах.\n\n\"Скажи честно, Стефан. Я сегодня выгляжу как уставшая трактирная девка или как девушка, на которую стоит смотреть дольше?\""
    $ CurLocDesc = MainTxt
    menu:
        "Сказать, что она выглядит красивой":
            $ Amanda.change_social(friend_delta=1, open_delta=1)
            $ Amanda.change_mana(1, "talk_look_praised")
            $ MainTxt = "Аманда улыбается слишком быстро, чтобы скрыть, как ей понравился ответ.\n\n\"Вот так и говори иногда. А то от одной работы можно забыть, что на тебя вообще смотрят как на девушку.\""
        "Сказать, что работа ей идет":
            $ Amanda.change_social(open_delta=1)
            $ MainTxt = "Аманда качает головой, но не злится.\n\n\"Работа мне идет, конечно. Только иногда хочется, чтобы заметили не поднос в руках, а меня саму.\""
        "Пошутить, что Сандра найдет ей еще работы":
            $ Amanda.change_mana(-1, "talk_look_bad_joke")
            $ relationship_set_anger("amanda", 1, 1, "bad_joke")
            $ MainTxt = "Аманда мгновенно хмурится.\n\n\"Ну да. Очень смешно. Тогда иди и сам поговори с Сандрой, раз тебе так весело.\""
    $ CurLocDesc = MainTxt
    return
