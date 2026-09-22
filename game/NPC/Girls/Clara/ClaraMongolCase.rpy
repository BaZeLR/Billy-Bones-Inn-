# Horse-theft accusation, distinct from Clarissa's later fiance case.
# The thread owns custody: reported -> fed -> released -> tavern arrival.

label story_clara_mongol_accusation:
    $ main_ui_begin_native_scene_state("Сообщница Монгола")
    show screen main_ui
    vscene "images/zimmer/portrait1.png"
    $ scene_runtime.text = "Вы вспоминаете ночной разговор Клариссы с Монголом. Теперь у вас есть возможность назвать Циммерману его сообщницу — или оставить её имя при себе."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Назвать Клариссу сообщницей Монгола":
            $ event_runtime.active_thread.advance()
            $ Mongol.zimmer_knows_horse_theft = True
            # An imprisoned Clara cannot play the wine-shop denial. Skip only
            # that pending step; do not pretend it was seen or rewind later play.
            if threads["claraBookletMarket"].num == 3:
                $ threads["claraBookletMarket"].num = 4
                $ threads["claraBookletMarket"].setDay()
            $ scene_runtime.text = "Вы называете Клариссу и пересказываете услышанное. Циммерман немедленно посылает стражников задержать её. Пока идёт расследование о конокрадстве, она останется под стражей."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Вернуться к разговору":
                    pass

        "Не выдавать Клариссу":
            $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
            $ event_runtime.active_thread.abort()
            $ scene_runtime.text = "Вы решаете не называть Клариссу. Это оставляет ей возможность доверять вам, но не означает, что теперь она откроет все свои тайны или откажется от собственных замыслов."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Вернуться к разговору":
                    pass

        "Пока ничего не решать":
            pass

    $ main_ui_end_native_scene_state()
    return True


label story_clara_mongol_custody:
    $ main_ui_begin_native_scene_state("Кларисса под стражей")
    show screen main_ui
    vscene "images/clara/portrait.png"
    if event_runtime.active_thread.num == 1:
        $ scene_runtime.text = "Вечером вы навещаете задержанную Клариссу. Она устала и голодна. Увидев вас, она первым делом спрашивает, не принесли ли вы еды."
    else:
        if str(Mongol.stocks_fate or "") in ("released", "convicted"):
            $ scene_runtime.text = "Кларисса всё ещё под стражей. Еду вы ей уже передали. Дело Монгола уже решено, и освободить их вместе теперь не получится."
        else:
            $ scene_runtime.text = "Кларисса всё ещё под стражей. Еду вы ей уже передали. Для общего побега нужно подготовить освобождение Монгола: раздобыть отмычки у Драупнира и отвлечь ночную стражу вином и ужином."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Передать Клариссе еду из трактира" if event_runtime.active_thread.num == 1 and int(player.tavern_management.productnum or 0) > 0:
            $ player.tavern_management.productnum -= 1
            $ event_runtime.active_thread.advance()
            $ scene_runtime.text = "Кларисса принимает еду. «На допросе я расскажу и о Легаре. Пусть не думает, будто отвечать за всё буду только я». Она замолкает, услышав шаги стражника."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Уйти от караулки":
                    pass

        "Уйти и вернуться позже":
            pass

    $ main_ui_end_native_scene_state()
    return True


label story_clara_mongol_tavern_arrival:
    $ main_ui_begin_native_scene_state("Кларисса возвращается в трактир")
    show screen main_ui
    vscene "images/clara/tavern_visit.png"
    $ scene_runtime.text = "После побега Кларисса приходит в трактир. Денег у неё не осталось, вернуться к Легаре она не хочет. Мелисса предлагает приютить её в своей комнате."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Выслушать Клариссу":
            pass
    $ scene_runtime.text = "«Дайте мне кров и работу, — просит Кларисса. — Я буду помогать по хозяйству». Она двигается осторожно и признаётся, что после прежнего наказания ей всё ещё больно."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Поселить у Мелиссы и поручить уборку со следующего дня":
            $ Clara.set_job_value("jobcleaningtomorrow", 1)
            $ event_runtime.active_thread.advance()

        "Обсудить это позже":
            pass
    $ main_ui_end_native_scene_state()
    return True
