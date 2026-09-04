# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label TavernProstClients(girl_name="", client_type=1, return_room=""):
    if str(return_room or "") == "":
        $ return_room = str(rooms.current_code or "TavernMain")
    if str(girl_name or "") == "":
        $ girl_name = str(rooms.get("TavernMain").state.get("client_room_girl", "") or "")
    if int(client_type or 0) != 1:
        return
    if str(girl_name or "") == "":
        $ main_ui_runtime.mode = "event"
        $ scene_runtime.text = "В отдельной комнате сейчас никого нет."
        $ scene_runtime.location_text = scene_runtime.text
        show screen main_ui
        menu:
            "Вернуться":
                return

    $ main_ui_runtime.mode = "event"
    $ scene_runtime.text = "Вы зашли в соседнюю комнату, где у вас было оборудовано специальное потайное окошко. Через него вам открылся прекрасный вид."
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Подсмотреть":
            call TavernProstClientsWatch(client_type, girl_name, return_room)
        "Вернуться":
            pass
    return


label TavernProstClientsWatch(client_type=1, girl_name="", return_room=""):
    $ renpy.dynamic("SexEventType")
    if str(return_room or "") == "":
        $ return_room = str(rooms.current_code or "TavernMain")
    if str(girl_name or "") == "":
        $ girl_name = str(rooms.get("TavernMain").state.get("client_room_girl", "") or "")
    if int(client_type or 0) != 1:
        return

    $ main_ui_runtime.mode = "event"
    $ main_ui_runtime.action_title = "Потайное окошко"
    $ main_ui_runtime.action_content = None
    $ SexEventType = int(GetSexEventFromTable(girl_name, 3, "Prostitution") or 0)

    if SexEventType <= 0:
        $ scene_runtime.text = "Вы осторожно проверяете потайное окошко, но в комнате сейчас никого нет."
        $ scene_runtime.location_text = scene_runtime.text
        show screen main_ui
        menu:
            "Вернуться":
                return

    if girl_name == "liza":
        $ Liza.portstreet_clients_seen_today = True
        $ Liza.has_seen_clients = True
        if SexEventType == 1:
            $ scene_runtime.text = "Вы видите юную мулатку отсасывающей у какого-то старика. Однако похотливый старикашка не удовлетворяется минетом и просит Лизетту лечь на кровать. Когда же девушка его послушалась, старый козел не колеблясь задрал ей платьице, стащил панталончики и загнал свой член в юную податливую плоть. Однако девчонке, судя по всему, такое пришлось по нраву - она начала с энтузиазмом подмахивать своему годящемуся ей в деды любовнику. Ее усилия не пропали даром - она вскоре кончила. А следом за ней кончил и старик. Мулаточка посмотрела на капающую из нее сперму и на ее мордашке отразилась озабоченность возможными последствиями."
            $ pregnancy_check("liza", "inside", 1, "", 1, "Неизвестный торговец")
            $ show_image_seq("liza", "portevents", "event1_", 3)
        elif SexEventType == 2:
            $ scene_runtime.text = "Вы видите как матрос-негр сел на край кровати и расстегнул штаны, высвобождая свой действительно огромный член. По лицу девочки пробежала тень сомнения, быстро сменившаяся решимостью. Лизетта скинула панталончики, задрала юбочку и села прямо на черный кол. Сначала в девочку вошла только головка, но постепенно в ней оказалась вся жердь. Затем она начинает сначала медленно, а затем все быстрее подниматься и опускаться. Негр не выдерживает ее скачки и начинает накачивать ее семенем. Вслед за ним кончает и Лизетта."
            $ pregnancy_check("liza", "inside", 1, "", 1, "Неизвестный негр")
            $ show_image("liza", "traktirevents", "event2_" + str(procedural_randint(1, 9, "tavern_client_liza_event2_%s" % int(current_game_day() or 0))))
        elif SexEventType == 99:
            $ scene_runtime.text = "Вы видите как юная Лизетта в очередной раз делает минет почтенному отцу семейства, мессиру Легаре. Виноторговец сначала спокойно сидит на краешке кровати, но вскоре входит в раж, хватает девочку за косички и начинает буквально трахать ее рот. Когда он кончает, мулатка чуть было не давится хлынувшей ей в горло спермой."
            $ pregnancy_check("liza", "mouth", 1, "legare")
            $ show_image("liza", "traktirevents", "event3_" + str(procedural_randint(1, 10, "tavern_client_liza_event3_%s" % int(current_game_day() or 0))))
        else:
            $ scene_runtime.text = "Вы видите как Лизетта отсасывает сразу у двух городских стражников. Вскоре один разряжается молодой шлюшке в ротик, а другой изукрашивает своей спермой ее смуглую мордашку."
            $ pregnancy_check("liza", "inside", 1, "", 1, "Неизвестный стражник")
            $ pregnancy_check("liza", "face", 1, "", 1, "Неизвестный стражник")
            $ show_image("liza", "traktirevents", "event4_" + str(procedural_randint(1, 6, "tavern_client_liza_event4_%s" % int(current_game_day() or 0))))
    else:
        $ Georgett.mark_portstreet_clients_seen()
        if SexEventType == 1:
            $ scene_runtime.text = "Вы видите стоящую раком, оперевшись о спинку кровати, Жоржетту. Ее короткая юбчонка задрана до пояса, а сзади ее наяривает огромный мужик, судя по одежде портовый грузчик. Наконец грузчик разряжается прямо в киску Жоржетты."
            $ pregnancy_check("georgett", "inside", 1, "", 1, "Неизвестный грузчик")
            $ show_image_seq("georgett", "portevents", "event1_", 3)
        elif SexEventType == 2:
            $ scene_runtime.text = "Вы видите как лежащую на кровати Жоржетту сношают в два смычка какие-то морячки. Причем тот, который трахает ее в киску - негр. Вдруг тело Жоржетты содрогается в оргазме. Через полминуты кончают и моряки, заливая ротик и киску девушки потоками своей спермы."
            $ pregnancy_check("georgett", "inside", 1, "", 1, "Неизвестный негр")
            $ pregnancy_check("georgett", "mouth", 1, "", 1, "Неизвестный моряк")
            $ show_image_seq("georgett", "portevents", "event2_", 3)
        elif SexEventType == 3:
            $ scene_runtime.text = "Вы видите как Жоржетта делает минет какому-то пацаненку. Перед самым оргазмом он вытаскивает свой членик и тугая струя измазывает хорошенькое личико Жоржетты."
            $ pregnancy_check("georgett", "mouthface", 1, "", 1, "Неизвестный горожанин")
            $ show_image_seq("georgett", "portevents", "event3_", 3)
        elif SexEventType == 99:
            if not threads["beckyEddieSex"].completed:
                if not Eddie.seen_with_georgett:
                    $ scene_runtime.text = "Вы видите голую Жоржетту с рыжим Эдди. Похоже, они играют в какую-то игру."
                    $ Eddie.seen_with_georgett = True
                else:
                    $ scene_runtime.text = "Вы видите Жоржетту с вашим знакомцем Эдди, играющих в уже знакомую вам игру."
                $ scene_runtime.text = scene_runtime.text + "\n\n\"Что это, негодный мальчишка? Неужто строгая леди-босс тебя так распалила?!\" - восклицает Жоржетта. Эдди смущенно отвечает, и через минуту эта игра заканчивается его бурной разрядкой.\n\n\"Хм, какой он озорник и фантазер,\" подумали вы и вернулись в зал трактира."
            else:
                $ scene_runtime.text = "Вы увидели как Эдди в очередной раз трахает Жоржетту. Их разговор быстро свелся к привычным оправданиям, стонам и финальному оргазму.\n\n\"Хм, какой он выдумщик,\" подумали вы и вернулись в зал трактира."
            $ pregnancy_check("georgett", "inside", 1, "eddie")
        else:
            $ scene_runtime.text = "Вы видите как Жоржетта лежит на кровати, откинувшись вниз, а городской стражник трахает ее между грудей. Наконец он разряжается прямо на груди шлюхи."
            $ pregnancy_check("georgett", "tits", 1, "", 1, "Неизвестный стражник")
            $ show_image_seq("georgett", "portevents", "event4_", 3)

    $ CleanSpermRandom(girl_name if girl_name else "georgett")
    $ calendar_v2.advance_minutes(40)
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Смотреть дальше" if CheckIfSexEventExist(girl_name, 3, "Prostitution") > 0:
            call TavernProstClientsWatch(client_type, girl_name, return_room)
        "Вернуться":
            pass
    return
