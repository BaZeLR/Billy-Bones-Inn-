# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:    
    def tavern_main_morning_event_data():
        event_pool = []

        if str(people.location("sandra") or "") == "TavernMain" and renpy.loadable("images/sandra/tavern/cleaning1.jpg"):
            event_pool.append({
                "picture": "images/sandra/tavern/cleaning1.jpg",
                "text": "Сандра уже выбралась в главный зал и сразу находит себе дело: поправляет лавки, оглядывает половицы и ворчит, что к полудню все должно выглядеть так, будто дом сам себя держит в порядке.",
            })

        if str(people.location("melissa") or "") == "TavernMain":
            melissa_hall_loadable = MelissaStaticData.image_sequence("tavern", "hall_cleaning")
            if len(melissa_hall_loadable) > 0:
                event_pool.append({
                    "picture": melissa_hall_loadable[int(current_game_day() + int(calendar_v2.hour or 0)) % len(melissa_hall_loadable)],
                    "text": "Мелисса тихо возится в зале, протирая столы и выправляя мелочи, которые вечером никто бы уже не заметил, а утром они сразу бросаются в глаза.",
                })

        if str(people.location("amanda") or "") == "TavernMain":
            amanda_hall_candidates = [
                "images/amanda/tavern/cleaning1.jpg",
                "images/amanda/tavern/cleaning2.jpg",
            ]
            amanda_hall_loadable = [row for row in amanda_hall_candidates if renpy.loadable(row)]
            if len(amanda_hall_loadable) > 0:
                event_pool.append({
                    "picture": amanda_hall_loadable[int(current_game_day() + int(calendar_v2.minute or 0)) % len(amanda_hall_loadable)],
                    "text": "Аманда носится по залу с утренней торопливостью, словно первые посетители уже вот-вот ввалятся с улицы, хотя до настоящей работы еще остается время.",
                })

        if str(people.location("amanda") or "") == "TavernMain" or str(people.location("melissa") or "") == "TavernMain":
            event_pool.append({
                "picture": "images/tavern/mainhall/bar_mainHall.png",
                "text": "Пока до открытия еще далеко, в зале больше всего возни у стойки: кто-то переставляет кружки и кувшины, кто-то протирает доски, а Аманда успевает суетиться сразу в нескольких местах.",
            })

        if str(people.location("sandra") or "") == "TavernMain":
            event_pool.append({
                "picture": "images/tavern/mainhall/camin_mainHall.png",
                "text": "Сандра заглядывает в зал и сразу замечает любую мелочь: где лавка стоит криво, где пепел не убран, а где к полудню понадобится еще дров и горячей воды.",
            })

        if str(people.location("sandra") or "") == "TavernStorage" or str(people.location("melissa") or "") == "Backyard" or str(people.location("amanda") or "") == "Backyard":
            event_pool.append({
                "picture": "images/tavern/mainhall/tavern_crew.jpg",
                "text": "Утренние хлопоты пока разбросаны по всему хозяйству: кто-то возится с припасами, кто-то занят двором, и весь дом живет скорее общим бытом, чем трактирной работой.",
            })

        event_pool.append({
            "picture": "images/tavern/mainhall/main_hall.png",
            "text": "Пока трактир еще не открылся, главная зала стоит почти пустой и тихой: только утренние приготовления напоминают, что к полудню здесь снова станет шумно.",
        })

        loadable_pool = []
        for row in list(event_pool or []):
            picture = str(dict(row or {}).get("picture", "") or "").strip()
            text = str(dict(row or {}).get("text", "") or "").strip()
            if picture != "" and renpy.loadable(picture):
                loadable_pool.append({"picture": picture, "text": text})

        if len(loadable_pool) <= 0:
            return {"picture": "images/tavern/mainhall/main_hall.png", "text": ""}

        try:
            event_index = int(current_game_day() + int(calendar_v2.hour or 0) + int(calendar_v2.minute or 0) + int(calendar_v2.day or 0) + int(calendar_v2.period or 0)) % len(loadable_pool)
        except Exception:
            event_index = 0
        return dict(loadable_pool[event_index] or {})

    def tavern_preopening_mode():
        return tavern_main_closed_text() == "" and int(calendar_v2.week or 0) != 7 and 6 <= int(calendar_v2.hour or 0) < 12

    def tavern_main_late_closed():
        current_hour = int(calendar_v2.hour or 0)
        return current_hour >= 23 or current_hour < 6

    def tavern_main_sunday_service_closed():
        return int(calendar_v2.week or 0) == 7

    def tavern_main_friday_dance_closed():
        return int(calendar_v2.week or 0) == 5 and 18 <= int(calendar_v2.hour or 0) < 22

    def tavern_main_open_hours_visible():
        return int(calendar_v2.week or 0) != 7 and not tavern_main_late_closed()

    def tavern_main_closed_text():
        if tavern_main_late_closed():
            return "Сейчас поздняя ночь и трактир закрыт, все спят. Ну а кто не спит - тот отдыхает. Но не в главной зале."
        if tavern_main_sunday_service_closed():
            return "Сейчас трактир закрыт, все ушли на службу в храм. Может вам тоже стоит пойти?"
        if tavern_main_friday_dance_closed():
            return "Сейчас трактир закрыт, все ушли пятничное общегородское празднование. Может вам тоже стоит пойти?"
        return ""

    def tavern_main_glory_hole_visible():
        return tavern_main_closed_text() == "" and player.tavern_management.glory_hole == 2

    def tavern_main_morning_routine_text():
        routine_pool = [
            "Сандра уже успела открыть ставни и теперь гоняет домашних, чтобы к полудню все выглядело прилично. Мелисса протирает столы, а Аманда то носит кувшины, то отвлекается на болтовню.",
            "Утренней суеты пока куда больше, чем настоящей работы: кто-то перетаскивает кувшины, кто-то вытряхивает тряпки, а Сандра с привычной строгостью следит, чтобы все не ленились.",
            "До настоящего наплыва гостей еще есть время, и потому в зале царит домашняя возня: столы выправляют, лавки двигают, а между делом успевают перекинуться парой слов и даже посмеяться.",
        ]
        if len(routine_pool) <= 0:
            return ""
        try:
            routine_index = int(current_game_day() + int(calendar_v2.day or 0) + int(calendar_v2.period or 0)) % len(routine_pool)
        except Exception:
            routine_index = 0
        return str(routine_pool[routine_index] or "")

    def tavern_main_preopening_background():
        return str(tavern_main_morning_event_data().get("picture", "") or "images/tavern/mainhall/main_hall.png")

    def tavern_main_morning_event_text():
        return str(tavern_main_morning_event_data().get("text", "") or "")

    def tavern_main_build_description():
        base_desc = str(rooms.get("TavernMain").descriptions[0].text or "")
        desc_parts = [base_desc]
        closed_text = tavern_main_closed_text()

        if closed_text:
            desc_parts.append(closed_text)
        else:
            if tavern_preopening_mode():
                desc_parts.append("Утро в трактире еще не перешло в обычный рабочий ритм. До полудня вы и ваши домочадцы только готовите зал, кухню и припасы к дневной суете.")
                desc_parts.append(tavern_main_morning_routine_text())
                desc_parts.append(tavern_main_morning_event_text())
                desc_parts.append("На кухне с утра возятся: " + str(tavern_household_present_names("TavernKitchen") or "никто") + ".")
                desc_parts.append("В зале сейчас видны: " + str(tavern_household_present_names("TavernMain") or "никто") + ".")
                desc_parts.append("По двору и кладовым шныряют: " + str(_tavern_join_names([name for name in ("sandra", "melissa", "amanda") if str(people.location(name) or "") in ("Backyard", "TavernStorage")]) or "никто") + ".")
                desc_parts.append("Сейчас как раз удобное время перекинуться с домашними парой слов, прежде чем начнется обычная работа.")
            else:
                desc_parts.append("На кухне в вашем трактире работают: " + str(NamesList("jobkitchen", "TavernKitchen") or "никто") + ".")
                desc_parts.append("За чистоту и порядок отвечают: " + str(NamesList("jobcleaning", "TavernMain") or "никто") + ".")
                desc_parts.append("Еду и выпивку пьяным, трезвым, похотливым, скромным и прочим посетителям разносят: " + str(NamesList("jobwaitress", "TavernMain") or "никто") + ".")
                desc_parts.append("Вы можете пообщаться с участницами своей команды через список персонажей справа.")

            if str(people.location("becky") or "") == "TavernMain":
                desc_parts.append("Бекки Блэнкеншип на этот раз сама заглянула к вам в трактир и присматривается к залу цепким хозяйским взглядом.")
            if str(people.location("georgett") or "") == "TavernMain":
                liza_work = int(Liza.job_value("jobwhore", 0) or 0) == 1
                georgett_work = int(Georgett.job_value("jobwhore", 0) or 0) == 1
                client_girl = str(rooms.get("TavernMain").state.get("client_room_girl", "") or "")
                if liza_work and georgett_work:
                    if client_girl == "georgett":
                        desc_parts.append("В правом углу трактира сидит юная Лизетта и ждет клиентов. А вот ее мамаша клиента уже похоже нашла.")
                    elif client_girl == "liza":
                        desc_parts.append("В правом углу трактира сидит Жоржетта и ждет клиентов. А вот ее старшую дочку, судя по всему, уже кто-то снял.")
                    else:
                        desc_parts.append("В правом углу трактира сидят Жоржетта со своей дочкой Лизеттой и ждут клиентов.")
                elif liza_work:
                    if client_girl == "liza":
                        desc_parts.append("В правом углу, где обычно сидит Лизетта, пусто. Похоже что ветренную девчонку уже кто-то снял.")
                    else:
                        desc_parts.append("В правом углу трактира сидит Лизетта и ждет клиентов.")
                elif georgett_work:
                    if client_girl == "georgett":
                        desc_parts.append("В правом углу, где обычно сидит Жоржетта, пусто. Похоже что шлюшку уже кто-то снял.")
                    else:
                        desc_parts.append("В правом углу трактира сидит Жоржетта и ждет клиентов.")
            glory_quest_started = bool(Draupnir.glory_hole_quote_received)
            if player.tavern_management.glory_hole == 1 and glory_quest_started:
                desc_parts.append("В дальнем углу трактира мастера Драупнир что-то строгает и пилит. Работа кипит. Еще несколько часов и вы сможете насладиться построенным глорихолом.")
            elif player.tavern_management.glory_hole == 2 and glory_quest_started:
                desc_parts.append("В дальнем углу трактира располагается ширмочка, а за ней, как вы знаете, глорихол - место где, за умеренную плату, а для вас, как вы надеетесь, и вовсе бесплатно, любой страждущий может получить полностью анонимный минет. Ну, если с другой стороны ширмы есть кто-то, желающий его сделать.")

        desc_parts.append(werecat_visible_text("TavernMain"))

        return "\n\n".join([part for part in desc_parts if str(part or "").strip()])

    TavernMainRoomDefinition = Room(
        code_name="TavernMain",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Главная зала трактира",
        bg_picture="images/tavern/mainhall/main_hall.png",
        descriptions=[
            RoomDescription(
                text="Главная зала трактира 'Дикий Жеребец'. В тускло освещенном зале стоят грубые, сбитые из досок столы и такие же скамьи. У дальнего конца виднеется барная стойка, а за ней проход на кухню. Слева двери ведущие в комнаты, где живут и отдыхают работники трактира. За вашей спиной выход на улицу. На стойке лежит большой и древний том, озаглавленный 'Бабслей и Литрбол для чайников'.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Пройти на кухню", target="TavernKitchen"),
            RoomExit(label="Выйти на улицу", target="StreetTavern"),
            RoomExit(label="Подняться наверх", target="TavernUpstairs"),
            RoomExit(label="Проверить конюшню", target="TavernStable"),
            RoomExit(label="Идти к глорихолу", target="TavernGloryHole", condition=tavern_main_glory_hole_visible),
        ],
        game_items=[
            "book_001",
            "fireplace_001",
            "bar_001",
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="06:00", end="22:59", condition=tavern_main_open_hours_visible),
        custom_properties={
            "hall_staff_jobs": ["jobkitchen", "jobcleaning", "jobwaitress"],
            "object_menu_label": "TavernMainObjectMenu",
        },
        state={
            "client_room_girl": "",
        },
    )

    def tavern_main_action_items():
        tavern_main_fireplace_wood_stock()
        sections = rooms.get("TavernMain").build_menu_sections()
        items = list(sections.get("movement", [])) + list(sections.get("actions", []))
        if tavern_main_closed_text() == "" and int(player.tavern_management.client_room_hole or 0) > 0 and str(rooms.get("TavernMain").state["client_room_girl"] or "") != "":
            items.append(MenuItem("Пойти проверить отдельную комнату", Call("TavernProstClients", rooms.get("TavernMain").state["client_room_girl"])))
        if tavern_main_closed_text() == "" and not tavern_preopening_mode() and story_event_available("TavernMain", "overheard"):
            items.append(MenuItem("Подслушать разговор в зале", Call("checkTriggers", "TavernMain", "overheard", 0)))
        if tavern_main_closed_text() == "" and story_event_available("TavernMain", "clara_paintings"):
            items.append(MenuItem("Поговорить с Клариссой о рисунках", Call("checkTriggers", "TavernMain", "clara_paintings", 0)))
        return items

label TavernMain:
    $ renpy.dynamic("_household_request_girl", "_household_request_type")
    $ renpy.dynamic("_tavern_main_base_desc", "_glory_quest_started", "_cur_desc_low", "_draupnir_gh_asked", "ShouldDispatchTavernEvent", "GirlNameTS1", "GirlNameTS2", "kitchenlist", "cleaninglist", "waitresslist", "_liza_whore_work", "_georgett_whore_work", "randvarPS", "_tavern_kids_description", "_tmp_bf_sandra", "_tmp_bf_amanda", "_tmp_bf_melissa", "_tmp_bf_georgett", "_tmp_bf_liza", "_tmp_kids_list")
    $ _tavern_main_base_desc = rooms.get("TavernMain").descriptions[0].text
    $ scene_runtime.text = _tavern_main_base_desc
    $ scene_runtime.location_text = _tavern_main_base_desc
    $ rooms.enter("TavernMain")
    $ tavern_main_fireplace_wood_stock()
    $ scene_runtime.picture = "images/tavern/mainhall/main_hall_night.png" if int(calendar_v2.hour or 0) >= 18 or int(calendar_v2.hour or 0) < 6 else "images/tavern/mainhall/main_hall.png"
    if tavern_preopening_mode():
        $ scene_runtime.picture = tavern_main_preopening_background()
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.talk_picture = ""
    $ main_ui_runtime.clear_contexts()
    $ main_ui_runtime.action_title = "Действия в трактире"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""
    python:
        # Force TavernMain base intro text in the left panel; prevents stale/conditional text bleed.
        _glory_quest_started = int(Draupnir.glory_hole_quote_received)
        _cur_desc_low = str(scene_runtime.location_text or "").lower()
        if ("глорихол" in _cur_desc_low) and _glory_quest_started <= 0:
            scene_runtime.text = _tavern_main_base_desc
            scene_runtime.location_text = _tavern_main_base_desc
    

    # Startup safety: no Glory Hole stage before the quest/dialog branch starts.
    if int(calendar_v2.week or 1) == 1 and int(calendar_v2.day or 1) == 1:
        $ _draupnir_gh_asked = int(Draupnir.glory_hole_quote_received)
        if _draupnir_gh_asked == 0:
            $ player.tavern_management.glory_hole = 0
            $ player.tavern_management.client_room_hole = 0
    # Determine if tavern is closed
    if tavern_main_closed_text() == "":
        python:
            rooms.get("TavernMain").state["client_room_girl"] = ""
            ShouldDispatchTavernEvent = (
                int(calendar_v2.week or 0) != 7
                and not tavern_preopening_mode()
            )
            if (
                ShouldDispatchTavernEvent
                and int(event_runtime.tavern_work_plan_day or -1) != current_game_day()
                and len(list(event_runtime.tavern_work_events or [])) == 0
                and len(list(event_runtime.tavern_played_today or [])) == 0
            ):
                tavern_work_build_daily_plan()

        if ShouldDispatchTavernEvent:
            call checkTriggers("TavernMain", "tavern_work", 0)
    
    $ GirlNameTS1 = "georgett"
    $ GirlNameTS2 = "liza"
    $ kitchenlist = NamesList("jobkitchen", "TavernKitchen")
    $ cleaninglist = NamesList("jobcleaning", "TavernMain")
    $ waitresslist = NamesList("jobwaitress", "TavernMain")

    # Main event and interaction logic
    if tavern_main_closed_text() == "":
        if str(people.location(GirlNameTS1) or "") == rooms.current_code:
            if calendar_v2.time_slot() == 3:
                call AddOthersSperm(GirlNameTS1, 7)
                call AddOthersSperm(GirlNameTS2, 8)
            $ _liza_whore_work = int(Liza.job_value("jobwhore", 0) or 0)
            $ _georgett_whore_work = int(Georgett.job_value("jobwhore", 0) or 0)
            if _liza_whore_work == 1 and _georgett_whore_work == 1:
                python:
                    randvarPS = procedural_randint(1, 5, key="procedural:Inn/TavernMain.rpy:procedural_randint:311:1")
                if randvarPS == 1 and CheckIfSexEventExist(GirlNameTS1, calendar_v2.time_slot()) > 0:
                    $ rooms.get("TavernMain").state["client_room_girl"] = "georgett"
                elif randvarPS == 2 and CheckIfSexEventExist(GirlNameTS2, calendar_v2.time_slot()) > 0:
                    $ rooms.get("TavernMain").state["client_room_girl"] = "liza"
            elif _liza_whore_work == 1:
                python:
                    randvarPS = procedural_randint(1, 3, key="procedural:Inn/TavernMain.rpy:procedural_randint:338:2")
                if randvarPS == 1 and CheckIfSexEventExist(GirlNameTS2, calendar_v2.time_slot()) > 0:
                    $ rooms.get("TavernMain").state["client_room_girl"] = "liza"
            elif _georgett_whore_work == 1:
                python:
                    randvarPS = procedural_randint(1, 3, key="procedural:Inn/TavernMain.rpy:procedural_randint:351:3")
                if randvarPS == 1 and CheckIfSexEventExist(GirlNameTS1, calendar_v2.time_slot()) > 0:
                    $ rooms.get("TavernMain").state["client_room_girl"] = "georgett"
        $ scene_runtime.picture = "images/tavern/mainhall/main_hall_night.png" if int(calendar_v2.hour or 0) >= 18 or int(calendar_v2.hour or 0) < 6 else "images/tavern/mainhall/main_hall.png"

    call RoomEnterEventGate(rooms.current_code, False)
    $ _tavern_kids_description = []
    if tavern_main_closed_text() == "" and not tavern_preopening_mode() and int(calendar_v2.week or 0) != 7:
        if str(people.location('amanda') or "") == rooms.current_code:
            call check_daily_event('amanda', None, rooms.current_code, calendar_v2.time_slot())
        if str(people.location('sandra') or "") == rooms.current_code:
            call check_daily_event('sandra', None, rooms.current_code, calendar_v2.time_slot())
        if str(people.location('melissa') or "") == rooms.current_code:
            call check_daily_event('melissa', None, rooms.current_code, calendar_v2.time_slot())
        $ _tmp_bf_sandra = DescribeBreastFeeding('sandra')
        if _tmp_bf_sandra:
            $ _tavern_kids_description.append(_tmp_bf_sandra)
        $ _tmp_bf_amanda = DescribeBreastFeeding('amanda')
        if _tmp_bf_amanda:
            $ _tavern_kids_description.append(_tmp_bf_amanda)
        $ _tmp_bf_melissa = DescribeBreastFeeding('melissa')
        if _tmp_bf_melissa:
            $ _tavern_kids_description.append(_tmp_bf_melissa)
        if str(people.location("georgett") or "") == rooms.current_code and int(Georgett.job_value("jobwhore", 0) or 0) == 1 and str(rooms.get("TavernMain").state["client_room_girl"] or "") != "georgett":
            $ _tmp_bf_georgett = DescribeBreastFeeding('georgett')
            if _tmp_bf_georgett:
                $ _tavern_kids_description.append(_tmp_bf_georgett)
        if str(people.location("liza") or "") == rooms.current_code and int(Liza.job_value("jobwhore", 0) or 0) == 1 and str(rooms.get("TavernMain").state["client_room_girl"] or "") != "liza":
            $ _tmp_bf_liza = DescribeBreastFeeding('liza')
            if _tmp_bf_liza:
                $ _tavern_kids_description.append(_tmp_bf_liza)
        if str(people.location("georgett") or "") == "TavernMain":
            $ _tmp_kids_list = ShowFullKidsListByAge('sandra','amanda','melissa','georgett','liza')
        else:
            $ _tmp_kids_list = ShowFullKidsListByAge('sandra','amanda','melissa')
        if _tmp_kids_list:
            $ _tavern_kids_description.append(_tmp_kids_list)
        if (str(people.location("georgett") or "") == rooms.current_code and int(Georgett.job_value("jobwhore", 0) or 0) == 1 and str(rooms.get("TavernMain").state["client_room_girl"] or "") != "georgett") or (str(people.location("georgett") or "") == rooms.current_code and calendar_v2.time_slot() < 2):
            call check_daily_event('georgett', None, rooms.current_code, calendar_v2.time_slot())
        if (str(people.location("liza") or "") == rooms.current_code and int(Liza.job_value("jobwhore", 0) or 0) == 1 and str(rooms.get("TavernMain").state["client_room_girl"] or "") != "liza") or (str(people.location("liza") or "") == rooms.current_code and calendar_v2.time_slot() < 2):
            call check_daily_event('liza', None, rooms.current_code, calendar_v2.time_slot())
    $ main_ui_runtime.action_title = "Действия в трактире"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_main_action_items()

    $ scene_runtime.location_text = tavern_main_build_description()
    if _tavern_kids_description:
        $ scene_runtime.location_text += "\n\n" + "\n\n".join(_tavern_kids_description)
    $ scene_runtime.text = scene_runtime.location_text

    if tavern_main_closed_text() == "":
        if story_event_available("TavernMain", "amanda_dress_request") and str(people.location("amanda") or "") == "TavernMain":
            call AmandaDressRequestEvent
        elif story_event_available("TavernMain", "melissa_dress_request") and str(people.location("melissa") or "") == "TavernMain":
            call MelissaDressRequestEvent
        else:
            python:
                _household_request_type, _household_request_girl = household_pending_request_girl("TavernMain")
            if str(_household_request_type or "") == "soap":
                call HouseholdSoapRequestEvent(_household_request_girl)

    while True:
        call screen main_ui


label TavernMainObjectMenu(object_id=""):
    $ renpy.dynamic("_room_object", "_tavern_object", "_tavern_room", "_tavern_action", "_tavern_args", "_tavern_label")
    $ tavern_main_fireplace_wood_stock()
    if str(object_id or "") != "":
        $ main_ui_runtime.object_id = object_id
    $ object_id = main_ui_runtime.object_id
    $ _tavern_object = None
    python:
        _tavern_room = rooms.current if rooms.current is not None else rooms.get("TavernMain")
        for _room_object in _tavern_room.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _tavern_object = _room_object
                break

    if _tavern_object is None:
        $ main_ui_runtime.action_items = tavern_main_action_items()
        return

    $ main_ui_runtime.object_id = object_id
    $ main_ui_runtime.action_title = str(_tavern_object.name or "Действия")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []  # Original
    if str(getattr(_tavern_object, "picture", "") or "").strip() and renpy.loadable(str(getattr(_tavern_object, "picture", "") or "").strip()):
        $ scene_runtime.picture = str(getattr(_tavern_object, "picture", "") or "").strip()
    if str(object_id or "") == "fireplace_001":
        $ scene_runtime.text = tavern_main_fireplace_description()
    else:
        $ scene_runtime.text = str(_tavern_object.description or "")
    $ scene_runtime.location_text = scene_runtime.text

    python:
        for _tavern_action in _tavern_object.visible_actions():
            _tavern_args = tuple(getattr(_tavern_action, "args", ()) or ())
            _tavern_label = str(_tavern_action.label or "")
            if str(getattr(_tavern_action, "action_id", "") or "") == "make_fire" and _pc_fire_is_active(TavernMainFireplaceObject):
                _tavern_label = "Подложить дрова"
            if _tavern_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_tavern_label, Call("TavernMainObjectText", object_id, _tavern_action.action_id)))
            elif _tavern_action.hook == "call" and str(_tavern_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_tavern_label, Call(_tavern_action.target, *_tavern_args)))
            elif _tavern_action.hook == "jump" and str(_tavern_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_tavern_label, Jump(_tavern_action.target)))
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "text", tavern_main_build_description()),
            SetField(scene_runtime, "location_text", tavern_main_build_description()),
            SetField(main_ui_runtime, "action_title", "Действия в трактире"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", tavern_main_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


label TavernMainObjectText(object_id="", action_id=""):
    $ renpy.dynamic("_room_action", "_room_object", "_tavern_name", "_tavern_room", "_tavern_text")
    python:
        _tavern_text = ""
        _tavern_name = ""
        _tavern_room = rooms.current if rooms.current is not None else rooms.get("TavernMain")
        for _room_object in _tavern_room.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _tavern_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _tavern_text = str(_room_action.target or "")
                    break
            break
        if _tavern_text:
            scene_runtime.text = _tavern_text
            scene_runtime.location_text = _tavern_text
            main_ui_runtime.action_title = _tavern_name or "Действия"
    call TavernMainObjectMenu(object_id)
    return

