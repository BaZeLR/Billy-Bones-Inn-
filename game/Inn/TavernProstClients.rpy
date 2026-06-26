# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label TavernProstClients(client_type=1, girl_name="", return_room=""):
    if str(return_room or "") == "":
        $ return_room = str(CurLoc or "TavernMain")
    if str(girl_name or "") == "":
        $ girl_name = str(TavernMainClientRoomGirl or "")
    if int(client_type or 0) != 1:
        jump expression str(return_room or "TavernMain")
    if str(girl_name or "") == "":
        $ UI_mode = "event"
        $ current_action_title = "Потайное окошко"
        $ current_action_content = None
        $ MainTxt = "В отдельной комнате сейчас никого нет."
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться", Jump(str(return_room or "TavernMain")))]
        call screen main_ui
        jump expression str(return_room or "TavernMain")

    $ UI_mode = "event"
    $ current_action_title = "Потайное окошко"
    $ current_action_content = None
    $ MainTxt = "Вы зашли в соседнюю комнату, где у вас было оборудовано специальное потайное окошко. Через него вам открылся прекрасный вид."
    $ CurLocDesc = MainTxt
    $ current_action_items = [MenuItem("Подсмотреть", Call("TavernProstClientsWatch", client_type, girl_name, return_room)), MenuItem("Вернуться", Jump(str(return_room or "TavernMain")))]
    call screen main_ui
    jump expression str(return_room or "TavernMain")


label TavernProstClientsWatch(client_type=1, girl_name="", return_room=""):
    if str(return_room or "") == "":
        $ return_room = str(CurLoc or "TavernMain")
    if str(girl_name or "") == "":
        $ girl_name = str(TavernMainClientRoomGirl or "")
    if int(client_type or 0) != 1:
        jump expression str(return_room or "TavernMain")

    $ UI_mode = "event"
    $ current_action_title = "Потайное окошко"
    $ current_action_content = None
    $ SexEventType = int(GetSexEventFromTable(girl_name, 3, "Prostitution") or 0)

    if SexEventType <= 0:
        $ MainTxt = "Вы осторожно проверяете потайное окошко, но в комнате сейчас никого нет."
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Вернуться", Jump(str(return_room or "TavernMain")))]
        call screen main_ui
        jump expression str(return_room or "TavernMain")

    if girl_name == "liza":
        $ Liza.mark_portstreet_clients_seen()
        if SexEventType == 1:
            $ MainTxt = "Вы видите юную мулатку отсасывающей у какого-то старика. Однако похотливый старикашка не удовлетворяется минетом и просит Лизетту лечь на кровать. Когда же девушка его послушалась, старый козел не колеблясь задрал ей платьице, стащил панталончики и загнал свой член в юную податливую плоть. Однако девчонке, судя по всему, такое пришлось по нраву - она начала с энтузиазмом подмахивать своему годящемуся ей в деды любовнику. Ее усилия не пропали даром - она вскоре кончила. А следом за ней кончил и старик. Мулаточка посмотрела на капающую из нее сперму и на ее мордашке отразилась озабоченность возможными последствиями."
            $ PregnancyCheck("liza", "inside", 1, "", 1, "Неизвестный торговец")
            $ ShowImageSeq("liza", "portevents", "event1_", 3)
        elif SexEventType == 2:
            $ MainTxt = "Вы видите как матрос-негр сел на край кровати и расстегнул штаны, высвобождая свой действительно огромный член. По лицу девочки пробежала тень сомнения, быстро сменившаяся решимостью. Лизетта скинула панталончики, задрала юбочку и села прямо на черный кол. Сначала в девочку вошла только головка, но постепенно в ней оказалась вся жердь. Затем она начинает сначала медленно, а затем все быстрее подниматься и опускаться. Негр не выдерживает ее скачки и начинает накачивать ее семенем. Вслед за ним кончает и Лизетта."
            $ PregnancyCheck("liza", "inside", 1, "", 1, "Неизвестный негр")
            $ ShowImage("liza", "traktirevents", "event2_" + str(procedural_randint(1, 9, "tavern_client_liza_event2_%s" % int(dayspassed or 0))))
        elif SexEventType == 99:
            $ MainTxt = "Вы видите как юная Лизетта в очередной раз делает минет почтенному отцу семейства, мессиру Легаре. Виноторговец сначала спокойно сидит на краешке кровати, но вскоре входит в раж, хватает девочку за косички и начинает буквально трахать ее рот. Когда он кончает, мулатка чуть было не давится хлынувшей ей в горло спермой."
            $ PregnancyCheck("liza", "mouth", 1, "legare")
            $ ShowImage("liza", "traktirevents", "event3_" + str(procedural_randint(1, 10, "tavern_client_liza_event3_%s" % int(dayspassed or 0))))
        else:
            $ MainTxt = "Вы видите как Лизетта отсасывает сразу у двух городских стражников. Вскоре один разряжается молодой шлюшке в ротик, а другой изукрашивает своей спермой ее смуглую мордашку."
            $ PregnancyCheck("liza", "inside", 1, "", 1, "Неизвестный стражник")
            $ PregnancyCheck("liza", "face", 1, "", 1, "Неизвестный стражник")
            $ ShowImage("liza", "traktirevents", "event4_" + str(procedural_randint(1, 6, "tavern_client_liza_event4_%s" % int(dayspassed or 0))))
    else:
        $ Georgett.mark_portstreet_clients_seen()
        if SexEventType == 1:
            $ MainTxt = "Вы видите стоящую раком, оперевшись о спинку кровати, Жоржетту. Ее короткая юбчонка задрана до пояса, а сзади ее наяривает огромный мужик, судя по одежде портовый грузчик. Наконец грузчик разряжается прямо в киску Жоржетты."
            $ PregnancyCheck("georgett", "inside", 1, "", 1, "Неизвестный грузчик")
            $ ShowImageSeq("georgett", "portevents", "event1_", 3)
        elif SexEventType == 2:
            $ MainTxt = "Вы видите как лежащую на кровати Жоржетту сношают в два смычка какие-то морячки. Причем тот, который трахает ее в киску - негр. Вдруг тело Жоржетты содрогается в оргазме. Через полминуты кончают и моряки, заливая ротик и киску девушки потоками своей спермы."
            $ PregnancyCheck("georgett", "inside", 1, "", 1, "Неизвестный негр")
            $ PregnancyCheck("georgett", "mouth", 1, "", 1, "Неизвестный моряк")
            $ ShowImageSeq("georgett", "portevents", "event2_", 3)
        elif SexEventType == 3:
            $ MainTxt = "Вы видите как Жоржетта делает минет какому-то пацаненку. Перед самым оргазмом он вытаскивает свой членик и тугая струя измазывает хорошенькое личико Жоржетты."
            $ PregnancyCheck("georgett", "mouthface", 1, "", 1, "Неизвестный горожанин")
            $ ShowImageSeq("georgett", "portevents", "event3_", 3)
        elif SexEventType == 99:
            if Becky.var.get("visitedhome", 0) < 7:
                if Eddie.var.get("SawWithGeorgett", 0) == 0:
                    $ MainTxt = "Вы видите голую Жоржетту с рыжим Эдди. Похоже, они играют в какую-то игру."
                    $ Eddie.var["SawWithGeorgett"] = 1
                else:
                    $ MainTxt = "Вы видите Жоржетту с вашим знакомцем Эдди, играющих в уже знакомую вам игру."
                $ MainTxt = MainTxt + "\n\n\"Что это, негодный мальчишка? Неужто строгая леди-босс тебя так распалила?!\" - восклицает Жоржетта. Эдди смущенно отвечает, и через минуту эта игра заканчивается его бурной разрядкой.\n\n\"Хм, какой он озорник и фантазер,\" подумали вы и вернулись в зал трактира."
            else:
                $ MainTxt = "Вы увидели как Эдди в очередной раз трахает Жоржетту. Их разговор быстро свелся к привычным оправданиям, стонам и финальному оргазму.\n\n\"Хм, какой он выдумщик,\" подумали вы и вернулись в зал трактира."
            $ PregnancyCheck("georgett", "inside", 1, "eddie")
        else:
            $ MainTxt = "Вы видите как Жоржетта лежит на кровати, откинувшись вниз, а городской стражник трахает ее между грудей. Наконец он разряжается прямо на груди шлюхи."
            $ PregnancyCheck("georgett", "tits", 1, "", 1, "Неизвестный стражник")
            $ ShowImageSeq("georgett", "portevents", "event4_", 3)

    $ CleanSpermRandom(girl_name if girl_name else "georgett")
    $ LastAdvancedMinutes = 40
    $ calendar_v2.advance_minutes(40)
    $ npc_schedule_sync_all()
    $ CurLocDesc = MainTxt
    $ current_action_items = []
    if CheckIfSexEventExist(girl_name, 3, "Prostitution") > 0:
        $ current_action_items.append(MenuItem("Смотреть дальше", Call("TavernProstClientsWatch", client_type, girl_name, return_room)))
    $ current_action_items.append(MenuItem("Вернуться", Jump(str(return_room or "TavernMain"))))
    call screen main_ui
    jump expression str(return_room or "TavernMain")
