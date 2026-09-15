# ================================================================================
# Robin camp destruction.
# The Robin thread owns event order; Zimmer owns complaint progress.
# ================================================================================

label story_robin_blackwood_camp_assault_0:
    $ renpy.dynamic("_robin_camp_outcome")
    $ main_ui_begin_native_scene_state("Лагерь Робина")
    show screen main_ui
    vscene "images/Robin/robin.png"
    $ scene_runtime.text = "После разговора с Циммерманом вы возвращаетесь на Шервудскую вырубку уже не ради торговли. За рядами пней видны навесы, костры и часовые: здесь устроилась вся шайка Робина. Пока этот лагерь стоит, нападения на дороге не прекратятся."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Разогнать шайку и уничтожить лагерь":
            pass

        "Отступить и подготовиться":
            $ scene_runtime.text = "Вы отходите от лагеря, не выдавая себя. Шайка остается на вырубке; сюда можно вернуться, когда вы будете готовы к драке."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Вернуться на дорогу":
                    pass
            $ main_ui_end_native_scene_state()
            return

    $ fight_begin("street_crook", 3, "BlackwoodRoad", "images/Robin/robin.png", "Вы выходите к кострам и требуете, чтобы люди Робина убирались с вырубки. В ответ трое вооруженных разбойников бросаются на вас, прикрывая отход остальных.")
    call FightLoop
    $ _robin_camp_outcome = str(fight.last_result.get("outcome", "") or "")
    vscene "images/Robin/robin.png"
    if _robin_camp_outcome == "victory":
        $ scene_runtime.text = "Последние разбойники бегут в лес. Вы валите навесы, тушите костры и уничтожаете оставленные припасы. Лагеря на Шервудской вырубке больше нет; теперь остается сообщить Циммерману."
        $ event_runtime.active_thread.advance()
    elif _robin_camp_outcome == "defeat":
        $ scene_runtime.text = "Разбойники оттесняют вас от костров. Вам удается выбраться на дорогу, но лагерь остается цел. Придется восстановить силы и вернуться."
    else:
        $ scene_runtime.text = "Вы разрываете бой и отходите к дороге. Лагерь Робина остается на месте; попытку придется повторить позже."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться на дорогу":
            pass
    $ main_ui_end_native_scene_state()
    return


label story_robin_blackwood_camp_report_1:
    $ main_ui_begin_native_scene_state("Разговор с Циммерманом")
    show screen main_ui
    vscene "images/zimmer/talk.png"
    $ scene_runtime.text = "Вы сообщаете Циммерману, что шайка разбита, а ее лагерь на Шервудской вырубке уничтожен.\n\n\"Вот видите, молодой человек, как хорошо мы с вами сработались,\" довольно отвечает десятник. \"Стража нашла лагерь, а вы решили оставшуюся маленькую практическую трудность. Теперь жалобу можно считать закрытой.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к разговору":
            pass
    $ Zimmer.robin_complaint_stage = 4
    $ Zimmer.mark_talked(1)
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True
