    $ npc_schedule_sync_all()label StreetClients(client_type=1, girl_name="", event_time=None):
    if event_time is None:
        $ event_time = calendar_v2.time_slot()
    call PortStreetsBackAlley(girl_name)
    jump PortStreetslabel StreetClients(client_type=1, girl_name="", event_time=None):
    if event_time is None:
        $ event_time = calendar_v2.time_slot()
    call PortStreetsBackAlley(girl_name)
    return
    $ npc_schedule_sync_all()label StreetClients(client_type=1, girl_name="", event_time=None):
    if event_time is None:
        $ event_time = calendar_v2.time_slot()
    call PortStreetsBackAlley(girl_name)
    jump PortStreetslabel StreetClients(client_type=1, girl_name="", event_time=None):
    if event_time is None:
        $ event_time = calendar_v2.time_slot()
    call PortStreetsBackAlley(girl_name)
    return
    $ npc_schedule_sync_all()label StreetClients(client_type=1, girl_name="", event_time=None):
    if event_time is None:
        $ event_time = calendar_v2.time_slot()
    call PortStreetsBackAlley(girl_name)
    jump PortStreetslabel StreetClients(client_type=1, girl_name="", event_time=None):
    if event_time is None:
        $ event_time = calendar_v2.time_slot()
    call PortStreetsBackAlley(girl_name)
    return
# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label StreetClients(client_type=1, girl_name="", event_time=None):
    if event_time is None:
        $ event_time = time
    call PortStreetsBackAlley(girl_name)
    jump PortStreets

label street_clients_watch(client_type=1, girl_name="", event_time=None):
    if int(client_type or 0) != 1:
        jump PortStreets

    $ CurrentRoom = PortStreetsRoom
    $ CurLoc = "PortStreets"
    $ UI_mode = "event"
    $ current_action_title = "Подворотня"
    $ current_action_content = None
    $ SexEventType = int(GetSexEventFromTable(girl_name, 3, "Prostitution") or 0)
    if SexEventType <= 0:
        $ MainTxt = "Вы осторожно проверяете переулок, но сегодня здесь уже нечего увидеть."
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться в переулок", Jump("PortStreets"))]
        call screen main_ui
        jump PortStreets

    if girl_name == "liza":
        $ Liza.mark_portstreet_clients_seen()
        if SexEventType == 1:
            $ MainTxt = "Вы видите юную мулатку отсасывающей у какого-то старика. Однако похотливый старикашка не удовлетворяется минетом и предлагает Лизетте наклониться и опереться о стену. Когда же девушка его послушалась, старый козел не колеблясь задрал ей платьице, спустил панталончики до колен и загнал свой член в юную податливую плоть. Однако девчонке, судя по всему, такое пришлось по нраву, и она с энтузиазмом подмахивает своему любовнику. Ее усилия не пропали даром. Вскоре кончает она, а следом и старик. Мулаточка смотрит на капающую из нее сперму и на ее мордашке отражается озабоченность возможными последствиями."
            $ pregnancy_check(girl_name, "inside", 1, "", 1, "Неизвестный торговец")
            $ _street_client_picture = build_media_ref(girl_name, "portevents", "event1_" + str(procedural_randint(1, 3, "street_client_liza_1_%s" % int(current_game_day() or 0))))
        elif SexEventType == 2:
            $ MainTxt = "Вы видите, как матрос-негр сел на какой-то топчан и расстегнул штаны, высвобождая действительно огромный член. По лицу девочки пробежала тень сомнения, быстро сменившаяся решимостью. Лизетта шустро скинула панталончики, задрала юбочку и села прямо на черный кол. Сначала в девочку вошла только головка, но постепенно, сантиметр за сантиметром, в ней оказалась вся жердь. Затем она начинает сначала медленно, а потом все быстрее подниматься и опускаться. На лице появляется блаженная улыбка. Негр не выдерживает ее скачки и начинает накачивать ее литрами своего семени. Вслед за ним кончает и Лизетта."
            $ pregnancy_check(girl_name, "inside", 1, "", 1, "Неизвестный негр")
            $ _street_client_picture = build_media_ref(girl_name, "portevents", "event2_" + str(procedural_randint(1, 3, "street_client_liza_2_%s" % int(current_game_day() or 0))))
        elif SexEventType == 99:
            if Alber.var_int("sawwithliza", 0) == 0:
                $ MainTxt = "Вы видите, как Лизетта делает минет кому-то смутно вам знакомому. Вскоре этот кто-то поворачивается, и вы узнаете мессира Легаре, почтенного отца семейства. Виноторговец входит в раж, хватает девочку за косички и начинает буквально трахать ее рот. Когда он кончает, мулатка чуть было не давится хлынувшей ей в горло спермой."
                $ Alber.set_var_int("sawwithliza", 1)
            else:
                $ MainTxt = "Вы видите, как юная Лизетта в очередной раз делает минет почтенному отцу семейства, мессиру Легаре. Виноторговец входит в раж, хватает девочку за косички и начинает буквально трахать ее рот. Когда он кончает, мулатка чуть было не давится хлынувшей ей в горло спермой."
            $ _street_client_picture = build_media_ref(girl_name, "portevents", "event3_" + str(procedural_randint(1, 4, "street_client_liza_3_%s" % int(current_game_day() or 0))))
            $ pregnancy_check(girl_name, "mouth", 1, "legare")
        else:
            $ MainTxt = "Вы видите, как Лизетта отсасывает сразу у двух городских стражников. Вскоре один разряжается молодой шлюшке в ротик, а другой изукрашивает своей спермой ее смуглую мордашку."
            $ pregnancy_check(girl_name, "inside", 1, "", 1, "Неизвестный стражник")
            $ pregnancy_check(girl_name, "face", 1, "", 1, "Неизвестный стражник")
            $ _street_client_picture = build_media_ref(girl_name, "portevents", "event4_" + str(procedural_randint(1, 4, "street_client_liza_4_%s" % int(current_game_day() or 0))))
    else:
        $ Georgett.mark_portstreet_clients_seen()
        if SexEventType == 1:
            $ MainTxt = "Вы видите стоящую раком Жоржетту. Ее короткая юбчонка задрана до пояса, а сзади ее наяривает огромный мужик, судя по одежде портовый грузчик. Шлюшка жалобно попискивает при каждом движении его огромного шланга. Наконец грузчик разряжается прямо в киску Жоржетты."
            $ pregnancy_check(girl_name, "inside", 1, "", 1, "Неизвестный грузчик")
            $ _street_client_picture = build_media_ref(girl_name, "portevents", "event1_" + str(procedural_randint(1, 3, "street_client_georgett_1_%s" % int(current_game_day() or 0))))
        elif SexEventType == 2:
            $ MainTxt = "Вы видите, как Жоржетту сношают в два смычка какие-то морячки. Причем тот, который трахает ее в киску, негр. Освобожденные от плена блузки сиськи шлюхи качаются в такт их движениям. Вдруг тело Жоржетты содрогается в оргазме. Через полминуты кончают и моряки, заливая ротик и киску девушки потоками своей спермы."
            $ pregnancy_check(girl_name, "inside", 1, "", 1, "Неизвестный негр")
            $ pregnancy_check(girl_name, "mouth", 1, "", 1, "Неизвестный моряк")
            $ _street_client_picture = build_media_ref(girl_name, "portevents", "event2_" + str(procedural_randint(1, 3, "street_client_georgett_2_%s" % int(current_game_day() or 0))))
        elif SexEventType == 3:
            $ MainTxt = "Вы видите, как Жоржетта делает минет какому-то пацаненку. Тому это явно нравится, и он приговаривает: \"Тетенька, сладко-то как! Хорошо-то как, тетенька!\" Перед самым оргазмом он вытаскивает свой членик, и тугая струя измазывает хорошенькое личико Жоржетты."
            $ pregnancy_check(girl_name, "mouthface", 1, "", 1, "Неизвестный горожанин")
            $ _street_client_picture = build_media_ref(girl_name, "portevents", "event3_" + str(procedural_randint(1, 3, "street_client_georgett_3_%s" % int(current_game_day() or 0))))
        elif SexEventType == 99:
            if Becky.var.get("visitedhome", 0) < 7:
                if Eddie.var.get("SawWithGeorgett", 0) == 0:
                    $ MainTxt = "Вы видите голую Жоржетту. Впрочем, зрелищем голой Жоржетты вас не удивишь, а вот тот факт, что она с вашим знакомцем рыжим Эдди, может и достоин внимания. Более того, похоже, они играют в какую-то игру."
                    $ Eddie.var["SawWithGeorgett"] = 1
                else:
                    $ MainTxt = "Вы видите Жоржетту с вашим приятелем Эдди, играющих в уже знакомую вам игру."
                $ MainTxt = MainTxt + "\n\n\"Что это, негодный мальчишка? Неужто это из-за меня?!\" - восклицает Жоржетта, указывая на вставший член Эдди.\n\n\"Мама, не сердись, но да, это из-за тебя! Как увидел тебя я обнаженной, так и не дает мне это зрелище покоя, не хочет мое мужское начало успокаиваться, причиняя мне страдания!\" - театрально восклицает вошедший в роль Эдди.\n\n\"Ах, что за негодный мальчишка мой сын!\" - несколько наигранно восклицает Жоржетта. \"Но что поделаешь, не могу же я заставить тебя мучаться!\"\n\nС этими словами она садится прямо на член вашего рыжего приятеля, впиваясь в него страстным поцелуем.\n\n\"А так легче, отпускает тебя напряжение?\" - спрашивает Жоржетта, ритмично двигаясь на члене парня.\n\n\"Еще нет, нет, нет, но отпускает, отпускает, отпускает!\" - кричит Эдди, спуская.\n\n\"Ах, негодник, прямо в меня спустил, а ведь я тебе запрещала!\" - строго говорит Жоржетта, но Эдди, находясь на вершине блаженства, ничего ей не отвечает.\n\n\"Хм, какой он озорник и фантазер,\" подумали вы и вернулись в переулок."
            else:
                $ MainTxt = "Вы увидели, как Эдди в очередной раз трахает Жоржетту.\n\n\"Что-то давненько ты ко мне захаживал,\" - осведомилась та у парня, двигаясь в такт его ритмичным толчкам. \"И в нашу маленькую игру играть не хочешь, и в дом к себе редко приглашаешь. Нашел, что ли, еще кого?\"\n\n\"Эээ, ну да, ой, то есть нет,\" - забормотал Эдди, продолжая трахать красотку. \"Просто дела идут сейчас не очень, не сезон, ну ты понимаешь, так что с деньгами у меня не очень,\" - продолжил он врать на ходу.\n\n\"Не заглядываешь ты ко мне, как начал мамку свою трахать, так я тебе и не нужна стала,\" - с присущим ей тактом прокомментировала Жоржетта поведение молодого бакалейщика.\n\n\"Эй, ну нет, то есть да,\" - смутился тот. \"Но ты не права, мамочка моя, конечно, лучшая и всегда теперь согласная, но и ты хороша. Да и разнообразие не помешает.\"\n\n\"Это точно,\" - согласилась шлюха. \"Ты на одной-то не зацикливайся. Если б я только один член бы трахала, меня бы тоска смертная, наверно, взяла. Так что пробуй разные дырки. Вот дочка моя, например, сейчас свободна,\" - перевела она разговор в деловое русло.\n\n\"Эээ, ну спасибо за совет, я, оооо, подумаю,\" - уклончиво ответил Эдди, спуская в Жоржетту.\n\n\"Хм, какой он выдумщик,\" подумали вы и вернулись в переулок."
            $ pregnancy_check(girl_name, "inside", 1, "eddie")
        else:
            $ MainTxt = "Вы видите, как Жоржетта стоит на коленях перед городским стражником, а тот трахает ее между грудей. Наконец он разряжается прямо на груди шлюхи. Крупные капли спермы стекают по ее стоящим соскам."
            $ pregnancy_check(girl_name, "tits", 1, "", 1, "Неизвестный стражник")
            $ _street_client_picture = build_media_ref(girl_name, "portevents", "event4_" + str(procedural_randint(1, 3, "street_client_georgett_4_%s" % int(current_game_day() or 0))))

    $ CleanSpermRandom(girl_name)
    $ calendar_v2.advance_minutes(40)
    $ CurLocDesc = MainTxt
    if str(_street_client_picture or "").strip():
        $ scene_image = str(_street_client_picture or "")
        $ _layout_last_picture = scene_image
        vscene scene_image
    $ current_action_items = []
    if CheckIfSexEventExist(girl_name, 3, "Prostitution") > 0:
        $ current_action_items.append(MenuItem("Смотреть дальше", Call("street_clients_watch", client_type, girl_name, event_time)))
    $ current_action_items.append(MenuItem("Вернуться в переулок", Jump("PortStreets")))
    call screen main_ui
    jump PortStreets

