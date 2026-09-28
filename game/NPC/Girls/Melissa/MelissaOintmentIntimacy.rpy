# Melissa's post-discipline ointment continuation.
# Availability and progress are owned only by melissaOintmentIntimacy.


label story_melissa_ointment_after_bats_0:
    $ main_ui_begin_native_scene_state("Просьба Мелиссы")
    show screen main_ui
    vscene MelissaStaticData.image_path("portrait", "default")
    $ scene_runtime.text = "Мелисса ловит вас наедине после дневных хлопот. «Я слышала о креме Серджио: после него кожа мягкая, словно шёлк. Приготовь и для меня. Я хочу почувствовать, как ты нанесёшь его сам». Она смотрит вам в глаза. «Аманда и Сандра умеют забрать всё твоё внимание. Я тоже хочу его — и не собираюсь делать вид, будто прошу только ради кожи»."
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

    $ scene_runtime.text = "Потом Лизетта вспоминает дорогой крем Серджио. «После него кожа такая мягкая, что самой хочется трогать. И наносить приятно: тепло от ладоней только сильнее кружит голову». Аманда фыркает: «А я думала, он годится лишь когда Сандра за розги хватается». — «Вот ещё! Он и после бритья хорош, и просто для красоты. Кто сказал, что за удовольствие надо сперва получить по заду?»"
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
    $ scene_runtime.text = "Поздно вечером в вашу дверь тихо стучит Мелисса. «Я пришла за кремом, — говорит она с порога. — Хочу, чтобы ты помог мне нанести его. Не на одну царапину, Стефан: на всю кожу. Никому другому я бы этого не доверила»."
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
    $ main_ui_begin_native_scene_state("Крем Серджио")
    show screen main_ui
    vscene MelissaStaticData.image_path("courtship", "storm_arrival")
    $ scene_runtime.text = "Мелисса приходит поздно вечером с чистым полотенцем. Увидев баночку, она запирает дверь. «Сегодня я хочу попробовать крем как следует. Только не спеши: мне нравится, когда ты обо мне заботишься»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Помочь Мелиссе нанести крем":
            if not player.remove_item("special_cream_001", 1):
                $ scene_runtime.text = "Вы не находите крема. Мелисса просит позвать её, когда новая баночка будет готова."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Проводить ее":
                        pass
                $ main_ui_end_native_scene_state()
                return True

            $ scene_runtime.text = "Вы согреваете крем между ладонями и проводите по плечам Мелиссы. Она удивлённо вздыхает: «Тёплый... и как приятно пахнет». Под вашими пальцами кожа становится гладкой; Мелисса всё меньше стесняется того, что ей нравятся и крем, и ваши руки."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Продолжить уход":
                    $ scene_runtime.text = "Вы растираете крем вдоль спины, затем на руках и ногах. Мелисса то смеётся от щекотки, то затихает, прислушиваясь к ощущениям. «Теперь понимаю, почему за эту баночку просят столько денег, — шепчет она. — Но приятнее всего, что наносишь её ты». Она просит не останавливаться, пока не кончится крем."
                    $ scene_runtime.location_text = scene_runtime.text
                    menu:
                        "Закончить и укрыть Мелиссу":
                            pass
                    vscene MelissaStaticData.image_path("portrait", "thanks")
                    $ scene_runtime.text = "Мелисса проводит ладонью по своей коже и довольно улыбается. «Мягкая. И я всё ещё чувствую тепло твоих рук». Она целует вас на прощание, обещая скоро снова прийти поговорить."
                    $ scene_runtime.location_text = scene_runtime.text
                    $ Melissa.set_sex_stat("beauty", min(100, int(Melissa.sex_stat("beauty", 0) or 0) + 2))
                    $ Melissa.add_arousal(8)
                    $ Melissa.change_social(friend_delta=1, open_delta=1)
                    $ calendar_v2.advance_minutes(40)
                    $ event_runtime.active_thread.advance()
                    $ event_runtime.evaluation_time = None
                    $ findAvailableEvents(True)

        "Отложить просьбу":
            $ scene_runtime.text = "Вы предлагаете вернуться к этому позже. Мелисса кивает; крем остаётся у вас."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Лечь спать":
                    pass

    $ main_ui_end_native_scene_state()
    return True
