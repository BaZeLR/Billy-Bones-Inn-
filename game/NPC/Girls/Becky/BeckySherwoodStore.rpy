# Becky owns the store invitation after Eddie's horse and purse are returned.
# The first invitation is a one-time event; the same scene can recur through talk.

label story_becky_sherwood_store_0:
    $ main_ui_begin_native_scene_state("Бекки: после Шервуда")
    show screen main_ui
    vscene grocery_store_grocer_picture("becky")
    $ scene_runtime.text = "Бекки обходит прилавок и на мгновение задерживает ваши руки в своих. «Ты вернул Эдди коня и деньги, Стефан. А мне — спокойный сон. За такое одним спасибо не отделаться. Если хочешь, дождись, пока в лавке никого не останется»."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Дождаться, пока лавка опустеет":
            $ main_ui_end_native_scene_state()
            call BeckySherwoodStorePrivateTime
            if _return:
                $ event_runtime.active_thread.advance()
                return True
            return False
        "Поблагодарить и вернуться к разговору":
            $ main_ui_end_native_scene_state()
            return False


label BeckySherwoodStorePrivateTime:
    $ main_ui_begin_native_scene_state("Наедине с Бекки")
    show screen main_ui
    vscene "images/becky/sex/kiss.jpg"
    $ scene_runtime.text = "Когда последний покупатель уходит, Бекки закрывает лавку изнутри и целует вас. «Дорогу ты расчистил, — шепчет она с улыбкой. — А теперь удели немного времени мне». Она ждёт вашего ответа, не отпуская руки."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Ответить на её поцелуй":
            pass
        "Оставить это на другой день":
            $ main_ui_end_native_scene_state()
            return False

    vscene "images/becky/sex/happy1.jpg"
    $ scene_runtime.text = "Вы остаётесь вдвоём. Когда Бекки снова отпирает дверь лавки, она поправляет волосы и, уже совсем не скрывая довольной улыбки, подмигивает вам из-за прилавка."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Закончить вместе":
            $ Becky.player_cum("inside")
        "Не рисковать беременностью":
            $ Becky.player_cum("outside")
    $ Becky.set_sex_busy(False)
    $ Becky.add_relation(1, cap=100)
    $ calendar_v2.advance_minutes(30)
    $ main_ui_end_native_scene_state()
    return True
