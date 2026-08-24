label IntDraupnirTalk:
    $ renpy.dynamic("_draupnir_talk_new")
    $ Draupnir.mark_known()
    $ _draupnir_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != "draupnir"
    $ main_ui_begin_talk_state("Разговор с Драупниром", "draupnir")
    if _draupnir_talk_new:
        $ scene_runtime.text = "Мастер Драупнир отрывается от работы и вопросительно смотрит на вас."
        $ scene_runtime.location_text = scene_runtime.text
    while True:
        menu:
            "Осмотреть":
                call StolyarWorkshopLook

            "Поболтать с гномом":
                $ scene_runtime.text = "Вы попробовали завести светскую беседу с гномом. С этой целью вы пнули пробегающую по мастерской крысу и заметили, что полетела она низко, видать к дождю. Еще пару минут вы развивали эту мысль, предсказывая по полету крысы обилие и частоту будущих осадков. Мастер Драупнир внимательно слушал вас некоторое, впрочем не очень долгое, время, а потом, разобравшись, оборвал: 'Слышь, мил человек, если у тебя есть чего сказать, то говори, ну а если нечего сказать, то и говорить необязательно.' Пораженный мудростью древнего народа вы решили замолкнуть."
                $ scene_runtime.location_text = scene_runtime.text

            "Спросить о ремонте вывески" if player.tavern_management.slogan_state == 0 and not Draupnir.slogan_quote_received:
                call StolyarWorkshopAskSlogan

            "Заплатить 200 мараведи за ремонт вывески" if player.tavern_management.slogan_state == 0 and Draupnir.slogan_quote_received and player.economy.money >= 200:
                call StolyarWorkshopPaySlogan

            "Спросить о дырке в стене" if int(Georgett.job_value("jobWhoreAvail", 0) or 0) > 0 and not Draupnir.peep_hole_quote_received and player.tavern_management.client_room_hole == 0:
                call StolyarWorkshopAskHole

            "Заплатить 100 мараведи за обзорное отверстие" if int(Georgett.job_value("jobWhoreAvail", 0) or 0) > 0 and Draupnir.peep_hole_quote_received and player.tavern_management.client_room_hole == 0 and player.economy.money >= 100 and rooms.get("StolyarWorkshop").is_open():
                call StolyarWorkshopPayHole

            "Спросить о глорихоле" if int(Georgett.job_value("jobWhoreAvail", 0) or 0) > 0 and not Draupnir.glory_hole_quote_received and player.tavern_management.glory_hole == 0 and int(Georgett.story_value("GloryHoleExplained", 0) or 0) == 1:
                call StolyarWorkshopAskGlory

            "Заплатить 700 мараведи за устройство глорихола" if int(Georgett.job_value("jobWhoreAvail", 0) or 0) > 0 and Draupnir.glory_hole_quote_received and player.tavern_management.glory_hole == 0 and player.economy.money >= 700 and rooms.get("StolyarWorkshop").is_open():
                call StolyarWorkshopPayGlory

            "Спросить о бочке для щелока" if soap_recipe_chain_discovered() and not crafting.ash_barrel_installed and not Draupnir.soap_barrel_quote_received:
                call StolyarWorkshopAskSoapBarrel

            "Заплатить 75 мараведи за зольную бочку" if soap_recipe_chain_discovered() and not crafting.ash_barrel_installed and Draupnir.soap_barrel_quote_received and player.economy.money >= 75 and rooms.get("StolyarWorkshop").is_open():
                call StolyarWorkshopPaySoapBarrel

            "Спросить о собачьей будке" if dog.owned and dog.booth_built == 0 and not Draupnir.dog_booth_quote_received:
                call StolyarWorkshopAskDogBooth

            "Заплатить 100 мараведи за собачью будку" if dog.owned and dog.booth_built == 0 and Draupnir.dog_booth_quote_received and player.economy.money >= 100 and rooms.get("StolyarWorkshop").is_open():
                call StolyarWorkshopPayDogBooth

            "Поговорить с Драупниром об отмычках" if story_event_available("StolyarWorkshop", "enter"):
                call checkTriggers("StolyarWorkshop", "enter", 0)

            "Назад":
                $ main_ui_end_talk_state()
                return
