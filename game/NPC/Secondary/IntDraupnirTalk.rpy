label IntDraupnirTalk:
    $ renpy.dynamic("_draupnir_talk_new")
    $ Draupnir.mark_known()
    $ _draupnir_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != "draupnir"
    $ main_ui_begin_talk_state("Разговор с Драупниром", "draupnir")
    if _draupnir_talk_new:
        $ scene_runtime.text = "Мастер Драупнир отрывается от работы и вопросительно смотрит на вас."
        $ scene_runtime.location_text = scene_runtime.text
    while True:
        menu:
            "Поболтать с гномом":
                $ scene_runtime.text = "Вы попробовали завести светскую беседу с гномом. С этой целью вы пнули пробегающую по мастерской крысу и заметили, что полетела она низко, видать к дождю. Еще пару минут вы развивали эту мысль, предсказывая по полету крысы обилие и частоту будущих осадков. Мастер Драупнир внимательно слушал вас некоторое, впрочем не очень долгое, время, а потом, разобравшись, оборвал: 'Слышь, мил человек, если у тебя есть чего сказать, то говори, ну а если нечего сказать, то и говорить необязательно.' Пораженный мудростью древнего народа вы решили замолкнуть."
                $ scene_runtime.location_text = scene_runtime.text

            "Назад":
                $ main_ui_end_talk_state()
                return
