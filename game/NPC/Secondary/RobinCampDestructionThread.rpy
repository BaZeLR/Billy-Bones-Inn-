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
        $ scene_runtime.text = "Последние разбойники бегут в лес. Вы валите навесы и тушите костры. У края стоянки остаются поваленные сундуки: в них можно будет порыться, когда уляжется дым. Лагеря на Шервудской вырубке больше нет; теперь остается сообщить Циммерману."
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
    if Eddie.fingal_talk_stage >= 2 or Becky.eddie_robbed_day > 0:
        $ scene_runtime.text += "\n\n\"И еще кое-что, — добавляет он. — Мои люди вывели оттуда коня Эдди и нашли его кошель. Деньги я не пересчитывал: пускай Эдди сам перед Бекки отчитается. Отведите ей и коня, и кошель.\""
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Вернуться к разговору":
            pass
    $ Zimmer.robin_complaint_stage = 4
    $ Zimmer.mark_talked(1)
    $ event_runtime.active_thread.advance()
    $ main_ui_end_native_scene_state()
    return True


label story_robin_blackwood_eddie_recovery_0:
    $ main_ui_begin_native_scene_state("Бекки: хорошие новости")
    show screen main_ui
    vscene grocery_store_becky_picture("becky")
    $ scene_runtime.text = "Вы заходите в лавку с поводом в одной руке и найденным кошелём в другой. Бекки сперва смотрит на вас, потом на знакомого коня за окном — и обеими ладонями упирается в прилавок, будто ей нужно удостовериться, что он настоящий.\n\n\"Конь Эдди? Целый? А это его деньги? Стефан, да ты не шутишь!\" Вы передаёте ей повод и кошель. Бекки прижимает кошель к себе, зовёт Эдди и долго смотрит, как тот проверяет сбрую. \"Циммерман рассказал, что вы сделали на вырубке. Спасибо тебе. Теперь можно снова возить товар в Куниделл, не гадая, кто вернётся домой.\"\n\nОна крепко обнимает вас у прилавка, не особенно заботясь о взглядах покупателей."
    $ scene_runtime.text += "\n\nК вечеру о свободной дороге судачат уже на рынке. Возчики обещают снова останавливаться у «Дикого жеребца», и слава вашего трактира разносится дальше городских ворот."
    $ scene_runtime.location_text = scene_runtime.text
    $ Becky.add_relation(2, cap=100)
    $ Becky.trust = min(100, int(Becky.trust or 0) + 1)
    $ player.tavern_management.visitors += 20
    $ player.economy.tavern_fame += 3
    $ Mongol.arrival_due_day = current_game_day() + 3
    $ event_runtime.active_thread.advance()
    menu:
        "Вернуться к покупкам":
            pass
    $ main_ui_end_native_scene_state()
    return True


label story_robin_blackwood_camp_loot_0:
    $ main_ui_begin_native_scene_state("Покинутый лагерь")
    show screen main_ui
    vscene "images/Robin/robin.png"
    $ scene_runtime.text = "На вырубке тихо. Обугленные жерди навесов еще пахнут дымом, а под промокшим пологом лежит забытый дорожный сундук. Замок сорван в спешке; внутри что-то негромко звякает."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Обыскать сундук":
            $ player.add_item("blackwood_smooth_plug_001", 1)
            $ player.add_item("blackwood_carved_toy_001", 1)
            $ player.add_item("blackwood_pigments_001", 1)
            $ player.add_item("blackwood_lingerie_001", 1)
            $ player.add_money(2000)
            $ scene_runtime.text = "В сундуке обнаружились полированная пробка, резная игрушка для взрослых, коробка ярких красок, тонкое кружевное бельё и кошель с двумя тысячами мараведи. Похоже, разбойники грабили не только обозы с овощами. Вы забираете находки: прежних хозяев здесь уже не сыскать."
            $ scene_runtime.location_text = scene_runtime.text
            $ event_runtime.active_thread.advance()
            menu:
                "Вернуться на дорогу":
                    pass
            $ main_ui_end_native_scene_state()
            return True

        "Не трогать чужой сундук":
            $ scene_runtime.text = "Вы оставляете сундук под пологом. Если передумаете, на вырубку можно вернуться."
            $ scene_runtime.location_text = scene_runtime.text
            menu:
                "Вернуться на дорогу":
                    pass
            $ main_ui_end_native_scene_state()
            return False
