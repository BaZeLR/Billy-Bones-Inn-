# Amanda's two numbered night-visit sequences. The thread owns their order.

label story_amanda_attic_night_visit_0:
    $ main_ui_begin_native_scene_state("Аманда ночью")
    show screen main_ui
    vscene "images/player_room/amandaVisits/amanda_visit_0.jpg"
    $ scene_runtime.text = "Из комнаты Аманды опять доносятся смешки и возня. Мелисса ночует там после вашего падения с чердака. Когда за стеной наконец стихает, дверь вашей комнаты тихо приоткрывается: это Аманда."
    menu:
        "Притвориться спящим":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_1.jpg"
    $ scene_runtime.text = "Аманда подходит к кровати. Похоже, она хотела проверить, как вы после падения, но теперь медлит и смотрит на вас куда внимательнее."
    menu:
        "Не шевелиться":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_2.jpg"
    $ scene_runtime.text = "Она берётся за край одеяла и на секунду замирает. Вы по-прежнему не выдаёте, что проснулись."
    menu:
        "Ждать":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_3 .jpg"
    $ scene_runtime.text = "Аманда приподнимает одеяло и видит вашу эрекцию."
    menu:
        "Не выдавать себя":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_4.jpg"
    $ scene_runtime.text = "Она не сразу отпускает ткань; любопытство на миг пересиливает смущение."
    menu:
        "Ждать":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_5.jpg"
    $ scene_runtime.text = "Из соседней комнаты раздаётся голос Мелиссы. Аманда вздрагивает и поспешно опускает одеяло."
    menu:
        "Продолжить":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_6.jpg"
    $ scene_runtime.text = "«Вот это да», — шепчет Аманда, закрывая рот ладонями."
    menu:
        "Продолжить":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_7.jpg"
    $ scene_runtime.text = "Она смотрит на вас ещё секунду, пытаясь понять, действительно ли вы спите."
    menu:
        "Продолжить":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_8.jpg"
    $ scene_runtime.text = "Аманда бесшумно выскальзывает за дверь и возвращается к Мелиссе. Вы слышите, как она снова шепчет что-то за стеной, но слов не разобрать."
    menu:
        "Уснуть":
            pass
    $ household.morning_state[_household_morning_state_key("amanda", current_game_day() + 1)] = {"issue": "sleepy", "resolved": 0, "indecent": 0}
    $ event_runtime.active_thread.setDay()
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_amanda_attic_night_visit_1:
    $ main_ui_begin_native_scene_state("Аманда снова приходит")
    show screen main_ui
    vscene "images/player_room/amandaVisits/amanda_visit_provoke_0.jpg"
    $ scene_runtime.text = "После разговора за завтраком о пропавшем рисованном буклете Аманда снова приходит к вам ночью. На этот раз она не делает вид, что ошиблась дверью."
    menu:
        "Выслушать её":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_provoke_1.jpg"
    $ scene_runtime.text = "«Мы оба теперь кое-что знаем друг о друге, — говорит она. — Только не вздумай рассказывать Мелиссе, что я сюда приходила»."
    menu:
        "Пообещать молчать":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_provoke_2.jpg"
    $ scene_runtime.text = "Аманда задерживается рядом и смеётся уже без прежней неловкости. Похоже, доверять вам ей стало легче."
    menu:
        "Продолжить":
            pass
    vscene "images/player_room/amandaVisits/amanda_visit_provoke_3.jpg"
    $ scene_runtime.text = "Перед уходом Аманда снова проверяет, как вы отреагируете. «Только Мелиссе ни слова», — напоминает она."
    menu:
        "Пожелать ей спокойной ночи":
            pass
    $ Amanda.change_social(friend_delta=1, corruption_delta=1)
    $ event_runtime.active_thread.setDay()
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
