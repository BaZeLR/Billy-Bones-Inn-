# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -1 python:
    import renpy.exports as renpy

    # Melissa bats arc progression lives in MelissaVar["bats_episode"].
    # Stage map:
    # 0 - no bat arc yet
    # 1 - breakfast complaint happened
    # 2 - player promised to help and scheduled the attic check
    # 3 - room holes were inspected
    # 4 - attic colony was found
    # 5 - attic window peek happened and the scandal can trigger
    # 6 - attic fall happened, Melissa moved out, drawings timer started
    # 7 - colony was smoked out; roof repair / final cleanup still pending
    # 8 - player reported completion to Melissa; arc finished

    def melissa_bats_stage():
        return max(0, int(MelissaVar.get("bats_episode", 0) or 0))

    def melissa_attic_picture_path():
        for picture_path in (
            "images/player_room/player_room_attic_1.png",
            "images/player_room/player_room_attic.png",
            "images/tavern/myroom/playr_room attic.png",
        ):
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def melissa_fall_picture_path():
        for picture_path in (
            "images/player_room/fell_from_attic.png",
            "images/tavern/myroom/fell_from_attic.png",
        ):
            if renpy.loadable(picture_path):
                return picture_path
        return ""

    def melissa_drawings_picture_paths():
        return [
            picture_path
            for picture_path in (
                "images/melissa/underBedsearch_0.png",
                "images/melissa/underBedsearch_1.png",
                "images/melissa/unerBedsearch_2.png",
            )
            if renpy.loadable(picture_path)
        ]

    def attic_neighbor_sex_scene_text():
        return "Там, не особенно заботясь о чужих глазах, молочник грубо и с явным азартом имеет собственную жену. До вас долетают приглушенные стоны, хлесткий ритм тел и влажный блеск обнаженной кожи."

    def amanda_attic_busted():
        return int(AmandaVar.get("attic_window_busted", 0) or 0) == 1 and melissa_bats_stage() >= 6

    def melissa_bats_repair_complete():
        repair_day = int(MelissaVar.get("roof_repair_complete_day", -1) or -1)
        return (
            melissa_bats_stage() >= 7
            and repair_day >= 0
            and int(dayspassed or 0) >= repair_day
        )

    def melissa_sync_room_problem_state():
        stage = melissa_bats_stage()
        if stage >= 8:
            MelissaVar["temp_room"] = ""
            MelissaVar["roof_repair_complete_day"] = -1
            MelissaVar["roof_repair_order_day"] = -1
        MelissaVar["bats_episode"] = stage
        return stage >= 8 or melissa_bats_repair_complete()

    def melissa_temp_room_active(room_code="", time_value=None):
        melissa_sync_room_problem_state()
        room_key = str(room_code or "").strip()
        temp_room = str(MelissaVar.get("temp_room", "") or "").strip()
        slot = int(time if time_value is None else time_value or 0)
        hour_num = int(hour or 0)
        if temp_room == "" or temp_room != room_key:
            return False
        if melissa_bats_stage() >= 8:
            return False
        scheduled_room = ""
        try:
            scheduled_room = str(npc_schedule_location("melissa", int(week or 0), slot) or "")
        except Exception:
            scheduled_room = ""
        if scheduled_room == "TavernMelissaRoom":
            return True
        return hour_num < 10

    def melissa_attic_scandal_ready():
        melissa_sync_room_problem_state()
        return (
            melissa_bats_stage() == 5
        )

    def melissa_drawings_scene_ready():
        return (
            melissa_bats_stage() >= 6
            and melissa_bats_stage() < 8
            and str(MelissaVar.get("temp_room", "") or "") == "TavernAmandaRoom"
            and int(MelissaVar.get("drawings_found", 0) or 0) == 0
            and int(dayspassed or 0) >= int(MelissaVar.get("drawings_ready_day", -1) or -1)
            and str(CurLoc or "") == "TavernMelissaRoom"
        )

    def melissa_drawings_return_ready():
        return (
            int(MelissaVar.get("drawings_found", 0) or 0) == 1
            and int(MelissaVar.get("drawings_returned", 0) or 0) == 0
        )

    def melissa_bat_attic_colony_event_ready():
        return (
            str(CurLoc or "") == "TavernAtic"
            and melissa_bats_stage() == 3
            and int(dayspassed or 0) >= int(MelissaVar.get("bat_attic_check_day", -1) or -1)
        )

    def melissa_bat_attic_window_event_ready():
        return (
            str(CurLoc or "") == "TavernAtic"
            and melissa_bats_stage() in (4, 5)
        )

    def melissa_bat_attic_cleanup_event_ready():
        return (
            str(CurLoc or "") == "TavernAtic"
            and melissa_bats_stage() >= 6
            and melissa_bats_stage() < 8
        )

    def melissa_bat_completion_talk_event_ready():
        return (
            str(CurLoc or "") == "TavernMain"
            and melissa_bats_completion_ready()
        )

    def melissa_bat_attic_event_caption():
        stage = melissa_bats_stage()
        if stage == 3:
            return "Осмотреть балки и щели под крышей"
        if stage == 4:
            return "Осмотреть маленькое слуховое окно над комнатой Аманды"
        if stage == 5:
            return "Вернуться к слуховому окну над комнатой Аманды"
        if stage < 7:
            if int(_player_item_count_by_id("bat_repellent_001") or 0) > 0:
                return "Выжечь гнездо дымной смесью"
            return "Осмотреть, как выкурить гнездо"
        if int(MelissaVar.get("roof_repair_order_day", -1) or -1) < 0:
            if int(money or 0) >= 1000:
                return "Заказать починку крыши за 1000"
            return "Прикинуть, сколько обойдется починка крыши"
        return "Осмотреть починку крыши"

    def melissa_bat_drawings_event_caption():
        return "Присмотреться, чем шуршит Мелисса у кровати"

    def melissa_bat_completion_talk_caption():
        return "Сказать Мелиссе, что с ее комнатой наконец покончено"

    def bat_repellent_recipe_unlocked():
        return (
            int(MelissaVar.get("bat_recipe_unlocked", 0) or 0) == 1
            or recipe_book_hidden_recipes_revealed()
        )

    def melissa_bats_completion_ready():
        melissa_sync_room_problem_state()
        return (
            melissa_bats_stage() == 7
            and melissa_bats_repair_complete()
            and int(MelissaVar.get("drawings_returned", 0) or 0) == 1
        )

    def melissa_apply_bats_completion_rewards():
        MelissaVar["bats_episode"] = 8
        MelissaVar["bats_completed"] = 1
        MelissaVar["bats_completion_day"] = int(dayspassed or 0)
        MelissaVar["temp_room"] = ""
        MelissaVar["room_returned"] = 1
        MelissaVar["sex_engine_unlocked"] = 1
        MelissaVar["roof_repair_complete_day"] = -1
        MelissaVar["roof_repair_order_day"] = -1
        MelissaVar["AskedMCToSolveRoomProblem"] = 0
        CurrentLoc["melissa"] = "TavernMelissaRoom"
        try:
            _melissa_bat_thread = threads.get("melissaBatProblem", None)
            if _melissa_bat_thread is not None:
                _melissa_bat_thread.complete()
        except Exception:
            pass
        try:
            evalTime = None
            findAvailableEvents(True)
        except Exception:
            pass

label MelissaBatBreakfastScene:
    # Stage 1: breakfast complaint happened.
    $ MelissaVar["bats_episode"] = max(int(MelissaVar.get("bats_episode", 0) or 0), 1)
    $ BreakfastToday = True
    $ TavernBreakfastLastDay = int(dayspassed or 0)
    $ TavernBreakfastDay = int(dayspassed or 0)
    $ TavernBreakfastPresentIds = ["sandra", "amanda"]
    $ TavernBreakfastEventActive = True
    hide screen main_ui
    vscene tavern_kitchen_breakfast_picture()
    if renpy.loadable("images/amanda/mock_talk.png"):
        call ShowImage("", "", "images/amanda/mock_talk.png")
    "Утренний стол уже накрыт, но одного места не хватает. Аманда первой с грохотом ставит кружку на стол: \"Да что ж это такое, эта девка опять в кровати? Наверняка мыши с крыльями всю ночь над ней плясали. Мелисса!!\" И тут же складывает язык похабной вилкой, изображая совсем не летучую охоту."
    "Сандра без разговоров отвешивает ей крепкий шлепок по заду: \"Рот свой придержи, бедовая!\""
    if renpy.loadable("images/amanda/kitchen_help.png"):
        call ShowImage("", "", "images/amanda/kitchen_help.png")
    "Аманда, потирая место удара, только смеется: \"А что? Дом скоро и правда станет ведьмовским логовом с такой дрянью под крышей.\""
    "Сандра уже серьезнее отвечает: \"С братом Герхардом поговорить надо бы. Хоть крыша у него в голове не лучше нашей, может по старой памяти что путное скажет.\""
    "В этот момент в кухню, зевая и еле переставляя ноги, входит Мелисса. Вид у нее злой и невыспавшийся. \"Этот старый извращенец? Да он в ведьмах не разбирается. Только и умеет, что глазеть на баб под видом заботы.\""
    "Аманда приподнимает бровь и расплывается в усмешке: \"Вот это уже интереснее...\""
    "Разговор расползается дальше сам собой, а у вас в голове остается одна ясная мысль: с ее комнатой придется разбираться всерьез."
    $ MainTxt = "Утренний стол уже накрыт, но одного места не хватает. Аманда первой с грохотом ставит кружку на стол: \"Да что ж это такое, эта девка опять в кровати? Наверняка мыши с крыльями всю ночь над ней плясали. Мелисса!!\" И тут же складывает язык похабной вилкой, изображая совсем не летучую охоту.\n\nСандра без разговоров отвешивает ей крепкий шлепок по заду: \"Рот свой придержи, бедовая!\"\n\nАманда, потирая место удара, только смеется: \"А что? Дом скоро и правда станет ведьмовским логовом с такой дрянью под крышей.\"\n\nСандра уже серьезнее отвечает: \"С братом Герхардом поговорить надо бы. Хоть крыша у него в голове не лучше нашей, может по старой памяти что путное скажет.\"\n\nВ этот момент в кухню, зевая и еле переставляя ноги, входит Мелисса. Вид у нее злой и невыспавшийся. \"Этот старый извращенец? Да он в ведьмах не разбирается. Только и умеет, что глазеть на баб под видом заботы.\"\n\nАманда приподнимает бровь и расплывается в усмешке: \"Вот это уже интереснее...\"\n\nРазговор расползается дальше сам собой, а у вас в голове остается одна ясная мысль: с ее комнатой придется разбираться всерьез."
    $ CurLocDesc = MainTxt
    $ TavernKitchenSavedText = MainTxt
    return


label MelissaNightNoiseScene:
    $ _layout_last_picture = tavern_melissa_room_picture() or _layout_last_picture
    $ current_action_title = "Шум в комнате Мелиссы"
    $ current_action_content = None
    $ MainTxt = "Проходя по коридору наверху, вы слышите из комнаты Мелиссы тревожный шум: скрип кровати, злой шепот и какое-то нервное шевеление под самым потолком. Заглянув внутрь, вы видите, что Мелисса не спит и сидит на кровати, зло глядя вверх.\n\n\"О, хорошо, что ты здесь,\" шепчет она почти сразу. \"Опять эта дрянь над головой возится. То шорох, то писк, то будто кто-то бегает по балкам. Я уже не знаю, что хуже: сам шум или то, что после такой ночи утром стоишь как пьяная. Если можешь, помоги мне с этим по-человечески.\""
    $ CurLocDesc = MainTxt
    $ current_action_items = [
        MenuItem("Сказать, что вы разберетесь с этим", Call("MelissaNightNoiseChoice", "promise")),
        MenuItem("Успокоить Мелиссу", Call("MelissaNightNoiseChoice", "comfort")),
        MenuItem("Оставить ее на сегодня в покое", Call("MelissaNightNoiseChoice", "leave")),
    ]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label MelissaNightNoiseChoice(choice_code=""):
    $ _melissa_noise_choice = str(choice_code or "").strip().lower()
    if _melissa_noise_choice == "comfort":
        $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
        $ MainTxt = "Вы говорите Мелиссе чуть тише и спокойнее, чем обычно, что на этот раз не отмахнетесь от ее жалоб. От этого она не перестает злиться на потолок, но по голосу слышно, что ей уже легче от одного того, что кто-то наконец воспринимает проблему всерьез."
        $ CurLocDesc = MainTxt
        call MelissaNightNoiseScene
        return
    if _melissa_noise_choice == "comfort_after":
        $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
        $ MainTxt = "Вы задерживаетесь еще на пару спокойных слов, и Мелисса наконец перестает вслушиваться в каждый шорох как в личное оскорбление. Она все еще зла на эту дрянь под крышей, но теперь хотя бы знает, что вы не бросили ее с этой бедой одну."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Комната Мелиссы"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Пожелать спокойной ночи", Call("MelissaNightNoiseGoodnight"))]
        $ _paged_text = str(MainTxt or "")
        call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
        return
    if _melissa_noise_choice == "leave":
        $ MainTxt = "Вы решаете пока не затягивать ночной разговор. Мелисса недовольно выдыхает, плотнее кутается в одеяло и снова косится на потолок."
        $ CurLocDesc = MainTxt
        call TavernUpstairsBuildActions
        return
    # Stage 2: player promised to help and scheduled the attic check.
    $ MelissaVar["AskedMCToSolveRoomProblem"] = 1
    $ MelissaVar["bats_episode"] = 2
    $ MelissaVar["bat_attic_check_day"] = max(int(MelissaVar.get("bat_attic_check_day", -1) or -1), int(dayspassed or 0))
    $ MainTxt = "Вы обещаете, что не ограничитесь одними словами: сейчас же посмотрите, откуда именно тянет и где под потолком проходят щели, а утром подниметесь на чердак над ее комнатой. Мелисса заметно успокаивается.\n\n\"Вот это уже похоже на дело,\" тихо говорит она. \"Только не откладывай до бесконечности.\""
    $ CurLocDesc = MainTxt
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Осмотреть потолок и щели в комнате", Call("MelissaNightNoiseInspect")),
        MenuItem("Успокоить Мелиссу перед сном", Call("MelissaNightNoiseChoice", "comfort_after")),
        MenuItem("Пожелать спокойной ночи", Call("MelissaNightNoiseGoodnight")),
    ]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label MelissaNightNoiseInspect:
    if melissa_bats_stage() < 2:
        call MelissaNightNoiseScene
        return
    # Stage 3: room holes were inspected.
    $ MelissaVar["bats_episode"] = 3
    $ MainTxt = "Вы внимательно осматриваете потолок и почти сразу находите то, на что Мелисса злилась не зря: под самым верхом видны мелкие щели и старые дыры в дереве, а оттуда тянет затхлым чердаком. Доски местами подгнили, обшивка перекосилась, и теперь уже очевидно, что дрянь лезет сюда сверху, а не только из самой комнаты.\n\nТеперь все ясно: утром надо лезть на чердак над комнатой Мелиссы и смотреть, что там развелось."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Успокоить Мелиссу перед сном", Call("MelissaNightNoiseChoice", "comfort_after")),
        MenuItem("Пожелать спокойной ночи", Call("MelissaNightNoiseGoodnight")),
    ]
    $ story_thread_advance_current()
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label MelissaNightNoiseGoodnight:
    $ MainTxt = "Вы желаете Мелиссе спокойной ночи и оставляете ее отдыхать. Теперь хотя бы ясно, что утром надо проверить чердак над ее комнатой."
    $ CurLocDesc = MainTxt
    call TavernUpstairsBuildActions
    return


label MelissaAtticFallScene:
    if not melissa_attic_scandal_ready():
        call TavernAticBuildActions
        return
    $ _fall_picture = melissa_fall_picture_path()
    if str(_fall_picture or "").strip():
        call ShowImage("", "", _fall_picture)
    # Stage 6: attic fall happened, Melissa moved out, drawings timer started.
    $ MelissaVar["bats_episode"] = max(int(MelissaVar.get("bats_episode", 0) or 0), 6)
    $ MelissaVar["drawings_ready_day"] = int(dayspassed or 0) + 2
    $ MelissaVar["temp_room"] = "TavernAmandaRoom"
    $ AmandaVar["attic_window_busted"] = 1
    $ Friends["melissa"] = max(0, int(Friends.get("melissa", 0) or 0) - 7)
    $ Friends["amanda"] = max(0, int(Friends.get("amanda", 0) or 0) - 5)
    $ notoriety = min(100, int(notoriety or 0) + 10)
    $ tavernfame = max(-20, int(tavernfame or 0) - 2)
    $ MainTxt = "Вы тянетесь вперед еще на полшага, стараясь удержать взгляд на слишком уж откровенной сцене за слуховым окном, но старое дерево под ногами не выдерживает. Доска жалобно трещит, потом ломается, и в следующий миг вас с грохотом несет вниз — вместе с пылью, щепками и куском прогнившего настила.\n\nВы проваливаетесь прямо в комнату Мелиссы. Удар выходит таким, что в ушах звенит, а над головой еще сыплется труха из пролома. Как назло, именно в этот момент сама Мелисса распахивает дверь: в руках у нее узел с вещами и одеяло, будто она и без того уже решила на эту ночь уйти спать куда подальше от своей кровати.\n\nОна переводит взгляд с пролома в потолке на вас, распластанного среди досок, и на ваше слишком уж очевидное состояние — и краснеет не то от злости, не то от унижения.\n\n\"Ты... ты извращенец!\" — срывается у нее голос. — \"Подглядывал оттуда? А потом еще и ко мне в комнату свалился?! Всё. Хватит. Сегодня же переберусь к Аманде. Там, по крайней мере, потолок на голову не падает!\"\n\nПохоже, объясняться сейчас бесполезно. История вышла слишком громкой и слишком стыдной."
    $ CurLocDesc = MainTxt
    $ CurrentRoom = TavernMelissaRoomRoom
    $ CurLoc = "TavernMelissaRoom"
    $ location = CurLoc
    $ story_thread_advance_current()
    $ current_action_title = "Комната Мелиссы"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Выбраться в коридор", Jump("TavernUpstairs"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label MelissaFindDrawingsScene:
    if not melissa_drawings_scene_ready():
        call TavernMelissaRoomBuildActions
        return
    $ MelissaVar["drawings_found"] = 1
    $ _drawings_picture_paths = melissa_drawings_picture_paths()
    $ _drawings_scene_lines = [
        "Пока Мелисса вынужденно ночует у Аманды, ее собственная комната остается непривычно тихой. Вы осматриваете ее внимательнее обычного: ларь, табурет, складки одеяла, щель между стеной и кроватью.",
        "Под кроватью Мелиссы, задвинутые почти к самой стене, обнаруживаются несколько рисованных листков. Манера уверенная, линии смелые, а сюжеты вовсе не девичьи. Похоже, это не просто чужая пошлость, а чей-то тайный заработок — или по крайней мере опасная забава.",
    ]
    if len(_drawings_picture_paths) > 0:
        call ShowImage("", "", _drawings_picture_paths[0])
    if len(_drawings_picture_paths) > 1:
        call ShowImage("", "", _drawings_picture_paths[1])
    if len(_drawings_picture_paths) > 2:
        call ShowImage("", "", _drawings_picture_paths[2])
    $ MainTxt = "\n\n".join(_drawings_scene_lines)
    $ CurLocDesc = MainTxt
    $ story_thread_advance_current()
    call TavernMelissaRoomBuildActions
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label MelissaAtticCleanupScene:
    if not melissa_bat_attic_cleanup_event_ready():
        call TavernAticBuildActions
        return
    $ current_action_title = "Чердак"
    $ current_action_content = None
    if melissa_bats_stage() < 7:
        if int(_player_item_count_by_id("bat_repellent_001") or 0) > 0:
            $ MainTxt = "Гнездовище под крышей уже найдено, и теперь осталось довести дело до конца: выкурить дрянь дымной смесью и не дать ей снова расползтись по щелям."
            $ current_action_items = [
                MenuItem("Выжечь гнездо дымной смесью", Call("MelissaBurnAtticColony")),
                MenuItem("Отступить от балок", Call("TavernAticBuildActions")),
            ]
        else:
            $ MainTxt = "Теперь уже ясно, что под крышей свилось настоящее гнездовище. Просто так его не вымести: сначала нужна едкая дымная смесь, чтобы выгнать всю эту дрянь из-под кровли."
            $ current_action_items = [MenuItem("Отступить от балок", Call("TavernAticBuildActions"))]
        $ CurLocDesc = MainTxt
        $ _paged_text = str(MainTxt or "")
        call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
        return
    if int(MelissaVar.get("roof_repair_order_day", -1) or -1) < 0:
        if int(money or 0) >= 1000:
            $ MainTxt = "Летучих мышей вы уже выкурили, но щели под крышей никуда не делись. Если не заказать починку сейчас, через несколько дней все это полезет обратно."
            $ current_action_items = [
                MenuItem("Заказать починку крыши за 1000", Call("MelissaOrderRoofRepair")),
                MenuItem("Оставить крышу как есть", Call("TavernAticBuildActions")),
            ]
        else:
            $ MainTxt = "Летучих мышей вы уже выкурили, но без починки крыши дело не закончить. Денег на мастеров пока не хватает."
            $ current_action_items = [MenuItem("Отойти от пролома", Call("TavernAticBuildActions"))]
        $ CurLocDesc = MainTxt
        $ _paged_text = str(MainTxt or "")
        call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
        return
    if not melissa_bats_repair_complete():
        $ _days_left = max(0, int(MelissaVar.get("roof_repair_complete_day", -1) or -1) - int(dayspassed or 0))
        $ MainTxt = "Крыша еще в работе. По свежим доскам и забитым щелям видно, что мастера уже начали, но до полного порядка придется подождать еще {} дн.".format(_days_left)
        $ CurLocDesc = MainTxt
        $ current_action_items = [MenuItem("Отойти от починки", Call("TavernAticBuildActions"))]
        $ _paged_text = str(MainTxt or "")
        call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
        return
    $ melissa_sync_room_problem_state()
    $ MainTxt = "Теперь на чердаке сразу видно, что работа завершена: щели закрыты, прогнившие доски заменены, а от старого гнездовища не осталось ничего, кроме сухой пыли. С комнатой Мелиссы наконец действительно покончено."
    $ CurLocDesc = MainTxt
    $ story_thread_advance_current()
    $ current_action_items = [MenuItem("Спуститься вниз", Call("TavernAticBuildActions"))]
    $ _paged_text = str(MainTxt or "")
    call QueuePagedPanelText(_paged_text, current_action_title, current_action_items, "plain")
    return


label MelissaReturnDrawingsScene:
    if not melissa_drawings_return_ready():
        call IntMelissaTalkRefresh("melissa")
        return
    call story_clara_paintings_melissa_0
    return


label MelissaBatsCompletionScene:
    if not melissa_bats_completion_ready():
        call IntMelissaTalkRefresh("melissa")
        return
    # Stage 8: player reported completion to Melissa; arc finished.
    $ melissa_apply_bats_completion_rewards()
    $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 3)
    $ otkroven["melissa"] = min(20, int(otkroven.get("melissa", 0) or 0) + 2)
    $ MainTxt = "Вы говорите Мелиссе, что на этот раз все действительно закончено: чердачное гнездовище выжжено, щели под крышей забиты, а над ее комнатой теперь наконец тихо. Она сперва смотрит на вас с привычной настороженностью, будто все еще ждет подвоха, но потом сама коротко выдыхает и впервые за все это время заметно расслабляется.\n\n\"Значит, можно снова спать у себя и не ждать, что ночью над головой начнут бегать, пищать и сыпать трухой...\" Она качает головой, будто сама до конца не верит в удачу, а потом уже тише добавляет: \"Спасибо. Не за слова — за то, что ты и правда довел дело до конца.\"\n\nПохоже, история с летучими мышами и чердаком для Мелиссы наконец действительно закрыта."
    $ CurLocDesc = MainTxt
    call IntMelissaTalkRefresh("melissa")
    return
