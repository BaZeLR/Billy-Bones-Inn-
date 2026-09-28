# Melissa's post-discipline ointment continuation.
# Availability and progress are owned only by melissaOintmentIntimacy.


label story_melissa_ointment_after_bats_0:
    $ main_ui_begin_native_scene_state("Просьба Мелиссы")
    show screen main_ui
    vscene MelissaStaticData.image_path("portrait", "default")
    $ scene_runtime.text = "Мелисса ловит вас наедине после дневных хлопот. «Ты помог Клариссе той мазью. Приготовь и для меня: она лечит кожу, а я хочу, чтобы твои руки наконец достались мне». Она смотрит вам в глаза. «Аманда и Сандра умеют забрать всё твоё внимание. Я тоже хочу его — и не собираюсь делать вид, что прошу только ради мази»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Пообещать поговорить об этом позже":
            $ calendar_v2.advance_minutes(10)
            $ event_runtime.active_thread.advance()
            $ event_runtime.evaluation_time = None
            $ findAvailableEvents(True)
        "Не давать обещания":
            $ scene_runtime.text = "Мелисса принимает ответ без спора. Если вы передумаете, она сможет вернуться к разговору в другой день."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Вернуться к делам":
                    pass
    $ main_ui_end_native_scene_state()
    return True


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
    $ scene_runtime.text = "Поздно вечером в вашу дверь тихо стучит Мелисса. «Я пришла за той мазью, — говорит она с порога. — Хочу попробовать её на чувствительной коже. И хочу, чтобы помог именно ты. Никому другому я бы такого не предложила»."
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
    $ scene_runtime.text = "Мелисса снова приходит поздно вечером. Увидев банку, она запирает дверь. «Нанеси мазь сам, Стефан. Я хочу почувствовать, помогает ли она. И не стану притворяться, будто мне не нравится твоя близость»."
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

            $ scene_runtime.text = "Вы наносите мазь; Мелисса привыкает к вашим прикосновениям и замечает, что раздражение проходит. «Я хочу попробовать анальный секс с тобой, — говорит она. — Но раньше я этого не делала. Боюсь, что будет больно. Если попрошу остановиться, ты остановишься»."
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
