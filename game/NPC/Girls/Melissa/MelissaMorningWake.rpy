# One authored morning scene per melissaMorningWake step. Illness does not own or reset this thread.

label story_melissa_morning_wake_0:
    $ main_ui_begin_native_scene_state("Утро Мелиссы")
    show screen main_ui
    vscene MelissaStaticData.cycle_image("tavern", "sleep", 4)
    $ scene_runtime.text = "Вы зовете Мелиссу. Она не отвечает, лишь прячется глубже под одеяло. Когда вы осторожно щекочете ее, она вскрикивает, поджимает ноги и, не удержавшись, смеется. Ночная рубашка задирается; Мелисса замечает ваше возбуждение. «Ну вот, Стефан. Теперь я тоже не смогу сделать вид, будто ничего не заметила», — говорит она."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Дать ей прийти в себя":
            $ Melissa.change_social(friend_delta=1, open_delta=1)
            $ Melissa.add_arousal(8)
            $ player_apply_arousal_trigger("melissa_wake_tickle", max(0, 75 - int(player.intimacy.arousal_value() or 0)))
            $ calendar_v2.advance_minutes(15)
            $ event_runtime.active_thread.advance()
            if household_morning_issue_type("melissa") == "sleepy":
                $ household_clear_morning_issue("melissa")
                $ Melissa.wear_day_clothes()
        "Оставить ее спать":
            pass
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    if rooms.current_code == "TavernMelissaRoom":
        $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_morning_wake_1:
    $ main_ui_begin_native_scene_state("Любопытство Мелиссы")
    show screen main_ui
    vscene MelissaStaticData.cycle_image("tavern", "sleep", 2)
    $ scene_runtime.text = "Мелисса помнит ваше неловкое утро и на этот раз не отводит глаз. «Я хочу посмотреть на твой член, Стефан. Просто посмотреть. Если позволишь». Она ждет ответа, не притворяясь, будто речь о чем-то другом."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Позволить ей посмотреть":
            $ scene_runtime.text = "Мелисса смотрит, потом поднимает на вас глаза. «Спасибо, что не торопишь. Мне интересно, но сегодня на этом остановимся»."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Согласиться":
                    pass
            $ Melissa.change_social(open_delta=1)
            $ calendar_v2.advance_minutes(15)
            $ event_runtime.active_thread.advance()
            if household_morning_issue_type("melissa") == "sleepy":
                $ household_clear_morning_issue("melissa")
                $ Melissa.wear_day_clothes()
        "Не продолжать":
            pass
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    if rooms.current_code == "TavernMelissaRoom":
        $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_morning_wake_2:
    $ main_ui_begin_native_scene_state("Мелисса просит прикоснуться")
    show screen main_ui
    vscene MelissaStaticData.cycle_image("tavern", "sleep", 2)
    $ scene_runtime.text = "«В прошлый раз я только смотрела, — говорит Мелисса. — Теперь хочу потрогать тебя. Можно? Если испугаюсь, сразу остановлюсь»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Разрешить прикосновение":
            $ scene_runtime.text = "Она ненадолго прикасается, затем отнимает руку. «Вот теперь я знаю, каково это. Не смейся: я еще не решила, что мне делать дальше»."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Не торопить ее":
                    pass
            $ Melissa.change_social(friend_delta=1, open_delta=1)
            $ calendar_v2.advance_minutes(15)
            $ event_runtime.active_thread.advance()
            if household_morning_issue_type("melissa") == "sleepy":
                $ household_clear_morning_issue("melissa")
                $ Melissa.wear_day_clothes()
        "Остановиться":
            pass
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    if rooms.current_code == "TavernMelissaRoom":
        $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_morning_wake_3:
    $ main_ui_begin_native_scene_state("Еще одно утро с Мелиссой")
    show screen main_ui
    vscene MelissaStaticData.cycle_image("tavern", "sleep", 4)
    $ scene_runtime.text = "«Я хочу подержать тебя подольше, — говорит Мелисса. — И да, ты можешь посмотреть на меня. Только не вздумай потом говорить, будто я не знала, чего хочу»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Дать ей самой задать темп":
            $ scene_runtime.text = "Мелисса задерживает руку, затем сама останавливается. «Сегодня хватит. А завтра я, может быть, осмелею еще больше», — говорит она, поправляя рубашку."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Оставить ее собираться":
                    pass
            $ Melissa.change_social(friend_delta=1, open_delta=1)
            $ calendar_v2.advance_minutes(20)
            $ event_runtime.active_thread.advance()
            if household_morning_issue_type("melissa") == "sleepy":
                $ household_clear_morning_issue("melissa")
                $ Melissa.wear_day_clothes()
        "Не продолжать":
            pass
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    if rooms.current_code == "TavernMelissaRoom":
        $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_morning_wake_4:
    $ main_ui_begin_native_scene_state("Мелисса решается")
    show screen main_ui
    vscene MelissaStaticData.image_path("sexy_times", "handjob")
    $ scene_runtime.text = "«Я хочу довести тебя до конца рукой, — прямо говорит Мелисса. — Не потому, что ты просил. Потому что сама хочу попробовать». Она заметно волнуется, но не отступает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Согласиться":
            $ scene_runtime.text = "На этот раз Мелисса не отступает после первого прикосновения. Позже она усмехается: «Теперь я знаю, что могу закончить начатое. А ты знаешь, что мы опоздаем к завтраку»."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Поблагодарить ее":
                    pass
            $ Melissa.player_cum("outside")
            $ player.intimacy.set_arousal(0)
            $ Melissa.change_social(friend_delta=1, open_delta=1, corruption_delta=1)
            $ calendar_v2.advance_minutes(20)
            $ event_runtime.active_thread.advance()
            if household_morning_issue_type("melissa") == "sleepy":
                $ household_clear_morning_issue("melissa")
                $ Melissa.wear_day_clothes()
        "Отложить":
            pass
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    if rooms.current_code == "TavernMelissaRoom":
        $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_morning_wake_5:
    $ main_ui_begin_native_scene_state("Новый шаг Мелиссы")
    show screen main_ui
    vscene MelissaStaticData.cycle_image("sexy_times", "blowjob", 0)
    $ scene_runtime.text = "«Я хочу попробовать ласкать тебя ртом, — говорит Мелисса без обычных отговорок. — Только не подгоняй меня. Если захочу остановиться, я остановлюсь»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Позволить ей попробовать":
            $ scene_runtime.text = "Мелисса пробует, затем сама отстраняется. «Да, я действительно этого хотела, — говорит она с удивленной улыбкой. — Но мне нужно время. В следующий раз я решу сама»."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Оставить ее собираться":
                    pass
            $ Melissa.change_social(friend_delta=1, open_delta=1)
            $ calendar_v2.advance_minutes(15)
            $ event_runtime.active_thread.advance()
            if household_morning_issue_type("melissa") == "sleepy":
                $ household_clear_morning_issue("melissa")
                $ Melissa.wear_day_clothes()
        "Подождать другого утра":
            pass
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    if rooms.current_code == "TavernMelissaRoom":
        $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    $ main_ui_end_native_scene_state()
    return True
