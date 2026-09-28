# One authored morning scene per melissaMorningWake step. Illness does not own or reset this thread.

label story_melissa_morning_wake_0:
    $ main_ui_begin_native_scene_state("Утро Мелиссы")
    show screen main_ui
    vscene MelissaStaticData.cycle_image("tavern", "sleep", 4)
    $ scene_runtime.text = "Вы зовете Мелиссу. Она не отвечает, лишь прячется глубже под одеяло. Когда вы осторожно щекочете ее, она вскрикивает, поджимает ноги и, не удержавшись, смеется. Сбитая ночная рубашка заставляет вас обоих смутиться; Мелисса замечает, как тесно стало в ваших штанах."
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
    $ scene_runtime.text = "Мелисса помнит ваше неловкое утро и теперь сама переводит взгляд на выпуклость под вашими штанами. Она спрашивает, позволите ли вы ей посмотреть поближе, без спешки и без обещаний продолжения."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Позволить ей посмотреть":
            $ scene_runtime.text = "Вы даете ей время удовлетворить любопытство. Потом Мелисса смущенно улыбается и просит оставить остальное на другой раз."
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
    $ scene_runtime.text = "В следующий раз Мелисса просит разрешения прикоснуться. Она проверяет вашу реакцию и заранее предупреждает, что остановится, когда сама захочет."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Разрешить прикосновение":
            $ scene_runtime.text = "Она пробует, быстро отнимает руку и смотрит на вас с тем самым любопытством, которое уже не умеет скрывать. На сегодня ей достаточно."
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
    $ scene_runtime.text = "Мелисса уже не делает вид, будто ее любопытство случайно. Она спрашивает, можно ли подержать вас чуть дольше, и в ответ сама позволяет вам разглядеть ее лучше. Решение, когда закончить, остается за ней."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Дать ей самой задать темп":
            $ scene_runtime.text = "Мелисса задерживает руку, затем смеется над собственной смелостью и останавливается. «Пока так», — говорит она, поправляя рубашку."
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
    $ scene_runtime.text = "Сегодня Мелисса сама предлагает продолжить начатую игру рукой. Она улыбается, хотя заметно волнуется, и ждет вашего ответа."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Согласиться":
            $ scene_runtime.text = "На этот раз она не отступает после первого прикосновения. Когда вы оба успокаиваетесь, Мелисса напоминает, что уже пора к завтраку."
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
    $ scene_runtime.text = "Позже Мелисса сама предлагает попробовать еще кое-что. Она просит не торопить ее и дать возможность остановиться в любой момент."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Позволить ей попробовать":
            $ scene_runtime.text = "Мелисса пробует, затем отстраняется и с удивленной улыбкой говорит, что ей нужно время привыкнуть к собственной решимости. Вы принимаете это без спора."
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
