# Clarissa's advice and Melissa's own choice are separate ordered events.
# This completion does not alter either girl's virginity.

label story_melissa_clara_solution_talk_0:
    $ main_ui_begin_native_scene_state("Совет Клариссы")
    show screen main_ui
    vscene "images/clara/melissa_talk.png"
    $ scene_runtime.text = "Кларисса замечает, что Мелисса снова смотрит на баночку с мазью, и без намеков говорит: «Я берегла девственность и выбирала анальный секс только с тем, кому доверяла. Мазь помогала коже, но не решала за меня, хочу ли я мужчину. Если ты хочешь попробовать со Стефаном, скажи ему сама и сразу оговори, когда он должен остановиться»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Выслушать ответ Мелиссы":
            pass
    $ scene_runtime.text = "Мелисса краснеет, но не прячется за Клариссой. «Да, хочу попробовать. Не ради твоих уроков и не потому, что мне надо кому-то что-то доказать. Я сама решу, когда и с кем». Кларисса одобрительно кивает и оставляет разговор вам двоим."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Согласиться ждать ее решения":
            $ calendar_v2.advance_minutes(15)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_clara_solution_1:
    $ main_ui_begin_native_scene_state("Решение Мелиссы")
    show screen main_ui
    vscene MelissaStaticData.image_path("tavern", "room")
    $ scene_runtime.text = "В другой вечер Мелисса сама возвращается к разговору. Она принесла мазь и говорит прямо: «Я хочу попробовать анальный секс с тобой. Но без спешки. Если скажу остановиться — остановишься. И моя девственность останется при мне»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Согласиться с ее условиями":
            if not player.remove_item("special_cream_001", 1):
                $ scene_runtime.text = "Мази под рукой нет. Мелисса предлагает вернуться к этому, когда вы приготовите новую баночку."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Подождать":
                        pass
                $ main_ui_end_native_scene_state()
                return True
            $ scene_runtime.text = "Вы остаетесь вдвоем. Мелисса задает темп, а вы останавливаетесь каждый раз, когда она просит. Позже она говорит, что ей понравилось быть услышанной и что это решение не изменило того, что она хотела сохранить."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Обнять Мелиссу":
                    pass
            $ Melissa.player_cum("outside")
            $ player.intimacy.set_arousal(0)
            $ Melissa.add_sex_stat("sexacts", 1)
            $ Melissa.mark_fucked(1)
            $ Melissa.record_orgasm_given()
            $ Melissa.record_sex_history("You", "TavernMelissaRoom", "outside")
            $ Melissa.change_social(friend_delta=2, open_delta=1)
            $ calendar_v2.advance_minutes(45)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
        "Подождать другого вечера":
            pass
    if rooms.current_code == "TavernMelissaRoom":
        $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    $ main_ui_end_native_scene_state()
    return True
