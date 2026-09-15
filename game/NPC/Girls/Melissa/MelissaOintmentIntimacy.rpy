# Melissa's post-discipline ointment continuation.
# Availability and progress are owned only by melissaOintmentIntimacy.


label story_melissa_ointment_talk_0:
    $ main_ui_begin_native_scene_state("Разговор Аманды и Лизетты")
    show screen main_ui
    vscene MelissaStaticData.image_path("courtship", "amanda_talk")
    $ scene_runtime.text = "Проходя мимо, вы слышите, как Аманда рассказывает Лизетте о наказании Сандры. Она сердито перечисляет и розги, и запрет встречаться с Легаре, но уже без прежнего вызова — похоже, после случившегося ей самой есть о чем подумать."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Продолжить слушать":
            pass

    $ scene_runtime.text = "Потом Аманда рассказывает Лизетте о лечебной мази, которой вы смазали следы от розги. \"Кожа после нее стала мягкой, и жечь перестало почти сразу,\" признается она. \"Такая мазь очень дорогая: помогает после бритья, успокаивает чувствительную кожу и даже лечит раздражение, если плохо вытереться.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Не выдавать своего присутствия":
            pass

    vscene MelissaStaticData.image_path("portrait", "default")
    $ scene_runtime.text = "Мелисса, занятая неподалеку, делает вид, что ничего не слышала. Но при словах о дорогой успокаивающей мази она заметно настораживается и несколько раз украдкой смотрит в вашу сторону."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к своим делам":
            pass

    $ calendar_v2.advance_minutes(10)
    $ event_runtime.active_thread.advance()
    $ event_runtime.evaluation_time = None
    $ findAvailableEvents(True)
    $ main_ui_end_native_scene_state()
    return True


label story_melissa_ointment_request_1:
    $ main_ui_begin_native_scene_state("Ночная просьба Мелиссы")
    show screen main_ui
    vscene MelissaStaticData.image_path("courtship", "storm_arrival")
    $ scene_runtime.text = "Поздно вечером в вашу дверь тихо стучит Мелисса. Она мнется на пороге, а затем признается, что слышала разговор Аманды с Лизеттой о дорогой лечебной мази. Ей хочется попробовать ее на чувствительной коже, но попросить об этом кого-нибудь другого она не решается."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пообещать помочь, когда мазь будет готова":
            $ scene_runtime.text = "Мелисса с облегчением кивает и просит никому не рассказывать о ее просьбе. Вы договариваетесь продолжить в одну из следующих поздних ночей, когда у вас будет банка лечебной мази."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Проводить ее до двери":
                    pass
            $ calendar_v2.advance_minutes(10)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)

        "Пока не обещать":
            $ scene_runtime.text = "Вы отвечаете, что пока не готовы обещать. Мелисса смущенно кивает и уходит; если вы передумаете, она сможет спросить снова другой ночью."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Лечь спать":
                    pass

    $ main_ui_end_native_scene_state()
    return True


label story_melissa_ointment_try_2:
    $ main_ui_begin_native_scene_state("Лечебная мазь")
    show screen main_ui
    vscene MelissaStaticData.image_path("courtship", "storm_arrival")
    $ scene_runtime.text = "Мелисса снова приходит поздно вечером. Увидев приготовленную банку, она запирает дверь и просит вас самому нанести мазь: одной ей неловко и неудобно добраться до чувствительной кожи."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Осторожно помочь Мелиссе":
            if not player.remove_item("special_cream_001", 1):
                $ scene_runtime.text = "Вы не находите лечебной мази. Мелисса просит позвать ее снова, когда средство будет готово."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Проводить ее":
                        pass
                $ main_ui_end_native_scene_state()
                return True

            $ scene_runtime.text = "Вы медленно втираете мазь, пока Мелисса привыкает к прикосновениям. Средство снимает раздражение и делает кожу мягче. Осмелев, она признается, что хочет попробовать анальную близость, но никогда прежде этого не делала и боится боли."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Попробовать очень осторожно":
                    vscene MelissaStaticData.image_path("portrait", "thanks")
                    $ scene_runtime.text = "Вы начинаете предельно медленно, но даже осторожная подготовка оказывается для Мелиссы болезненной. Она просит остановиться еще до проникновения. Вы тут же прекращаете, не настаивая; теперь оба знаете, что к настоящей попытке придется готовиться терпеливо."
                    $ scene_runtime.location_text = scene_runtime.text
                    menu:
                        "Обнять и успокоить ее":
                            pass
                    $ calendar_v2.advance_minutes(30)
                    $ event_runtime.active_thread.advance()
                    $ event_runtime.evaluation_time = None
                    $ findAvailableEvents(True)

        "Отложить просьбу":
            $ scene_runtime.text = "Вы предлагаете вернуться к этому позже. Мелисса кивает и уносит свою просьбу с собой; мазь остается у вас."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Лечь спать":
                    pass

    $ main_ui_end_native_scene_state()
    return True
