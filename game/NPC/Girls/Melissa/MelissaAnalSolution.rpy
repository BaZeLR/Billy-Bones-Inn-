# The overheard conversation follows Melissa's cream session; the shared
# full-moon visit follows the conversation. Neither event changes virginity.

label story_melissa_clara_solution_talk_0:
    $ main_ui_begin_native_scene_state("Разговор за дверью")
    show screen main_ui
    vscene "images/clara/melissa_talk.png"
    $ scene_runtime.text = "У двери комнаты Мелиссы вы слышите её смех и голос Клариссы. «Ну как крем? — спрашивает Кларисса. — Я же говорила: кожа становится шёлковой, а когда тебе помогают ласковые руки, приятен сам уход». Мелисса отвечает не сразу: «Он был так внимателен, что я теперь думаю о нём даже ночью. А этот стук под крышей опять не даёт уснуть»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Прислушаться к их разговору":
            pass
    $ scene_runtime.text = "Кларисса говорит тише: «Я тоже слышу его перед полнолунием. И я по-прежнему берегу девственность. Если мы обе решим быть со Стефаном, есть другой способ сблизиться, не переступая эту черту. Но ни крем, ни луна не должны решать за нас». Мелисса отвечает: «Тогда давай сперва спросим его самого». Дверь распахивается. «Стефан, заходи, — зовёт Кларисса. — Это касается нас троих»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Войти и выслушать обеих":
            $ scene_runtime.text = "Мелисса прямо говорит, что хочет продолжить вашу близость; Кларисса поддерживает её, но обе настаивают на своих границах. Вы обещаете дождаться их решения и остановиться по первому слову. Кларисса косится на окно: «Если шум снова придёт в полнолуние, мы найдём тебя сами»."
            $ scene_runtime.location_text = scene_runtime.text
            $ calendar_v2.advance_minutes(15)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_clara_solution_1:
    $ main_ui_begin_native_scene_state("Полнолуние: Мелисса и Кларисса")
    show screen main_ui
    vscene player_room_image_path("room")
    $ scene_runtime.text = "В полнолуние стук под крышей возвращается. В вашу дверь одновременно стучат Мелисса и Кларисса. Они пришли вместе и не собираются оставлять друг друга наедине с этим страхом. Кларисса ставит на стол баночку крема. «Мы обе хотим быть с тобой, Стефан, — говорит она. — Но сохраним девственность. Если кому-то станет не по себе, остановимся сразу». Мелисса берёт её за руку и кивает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Согласиться на их условия":
            if not player.remove_item("special_cream_001", 1):
                $ scene_runtime.text = "Крема под рукой нет. Кларисса предлагает не торопиться и встретиться снова в следующую полную луну, когда вы приготовите новую баночку."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Подождать следующего полнолуния":
                        pass
                $ main_ui_end_native_scene_state()
                return True
            $ scene_runtime.text = "Вы остаётесь втроём. Крем смягчает кожу, а каждая из девушек сама говорит, чего хочет и когда нужно замедлиться. Вы не выходите за оговорённые границы. Позже Мелисса, уже не слыша стука, устраивается рядом с Клариссой. «Мы сами выбрали этот вечер, — говорит она. — И своё слово сдержали». Кларисса отвечает: «Пусть луна только попробует спорить»."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Остаться с ними до утра":
                    pass
            $ Melissa.player_cum("outside")
            $ player.intimacy.set_arousal(0)
            $ Clara.add_sex_stat("sexacts", 1)
            $ Clara.mark_fucked(1)
            $ Clara.set_sex_busy(True)
            $ Melissa.record_orgasm_given()
            $ Melissa.record_sex_history("You", "TavernMyRoom", "outside")
            $ Clara.record_sex_history("You", "TavernMyRoom", "outside")
            $ Melissa.change_social(friend_delta=2, open_delta=1)
            $ Clara.change_social(friend_delta=2, open_delta=1)
            $ calendar_v2.advance_minutes(45)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
        "Предложить дождаться следующего полнолуния":
            pass
    $ main_ui_end_native_scene_state()
    return True
