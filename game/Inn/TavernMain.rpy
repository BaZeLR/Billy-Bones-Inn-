default TavernClosed = ""
#default TavernGloryHole = 0
default TavernEventOngoing = ""
default GeorgettAvail = 0
default LizaAvail = 0
default TavernMainExtraDesc = ""
default TavernMainGloryDesc = ""


init python:    
    def tavern_main_morning_event_data():
        event_pool = []

        if _tavern_is_in_room("sandra", "TavernMain") and renpy.loadable("images/sandra/tavern/cleaning1.jpg"):
            event_pool.append({
                "picture": "images/sandra/tavern/cleaning1.jpg",
                "text": "Сандра уже выбралась в главный зал и сразу находит себе дело: поправляет лавки, оглядывает половицы и ворчит, что к полудню все должно выглядеть так, будто дом сам себя держит в порядке.",
            })

        if _tavern_is_in_room("melissa", "TavernMain"):
            melissa_hall_candidates = [
                "images/melissa/tavern/melissa_cleans_0.png",
                "images/melissa/tavern/melissa_cleans_1.png",
            ]
            melissa_hall_loadable = [row for row in melissa_hall_candidates if renpy.loadable(row)]
            if len(melissa_hall_loadable) > 0:
                event_pool.append({
                    "picture": melissa_hall_loadable[int((dayspassed or 0) + (hour or 0)) % len(melissa_hall_loadable)],
                    "text": "Мелисса тихо возится в зале, протирая столы и выправляя мелочи, которые вечером никто бы уже не заметил, а утром они сразу бросаются в глаза.",
                })

        if _tavern_is_in_room("amanda", "TavernMain"):
            amanda_hall_candidates = [
                "images/amanda/tavern/cleaning1.jpg",
                "images/amanda/tavern/cleaning2.jpg",
            ]
            amanda_hall_loadable = [row for row in amanda_hall_candidates if renpy.loadable(row)]
            if len(amanda_hall_loadable) > 0:
                event_pool.append({
                    "picture": amanda_hall_loadable[int((dayspassed or 0) + (minute or 0)) % len(amanda_hall_loadable)],
                    "text": "Аманда носится по залу с утренней торопливостью, словно первые посетители уже вот-вот ввалятся с улицы, хотя до настоящей работы еще остается время.",
                })

        if _tavern_is_in_room("amanda", "TavernMain") or _tavern_is_in_room("melissa", "TavernMain"):
            event_pool.append({
                "picture": "images/tavern/mainhall/bar_mainHall.png",
                "text": "Пока до открытия еще далеко, в зале больше всего возни у стойки: кто-то переставляет кружки и кувшины, кто-то протирает доски, а Аманда успевает суетиться сразу в нескольких местах.",
            })

        if _tavern_is_in_room("sandra", "TavernMain"):
            event_pool.append({
                "picture": "images/tavern/mainhall/camin_mainHall.png",
                "text": "Сандра заглядывает в зал и сразу замечает любую мелочь: где лавка стоит криво, где пепел не убран, а где к полудню понадобится еще дров и горячей воды.",
            })

        if _tavern_is_in_room("sandra", "TavernStorage") or _tavern_is_in_room("melissa", "Backyard") or _tavern_is_in_room("amanda", "Backyard"):
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
            event_index = int((dayspassed or 0) + (hour or 0) + (minute or 0) + (day or 0) + (month or 0)) % len(loadable_pool)
        except Exception:
            event_index = 0
        return dict(loadable_pool[event_index] or {})

    def tavern_preopening_mode():
        return str(TavernClosed or "") == "" and int(week or 0) != 7 and int(time or 0) < 4 and int(hour or 0) < 12

    def tavern_main_glory_hole_visible():
        return TavernClosed == "" and TavernGloryHole == 2

    def tavern_main_sandra_visible():
        return TavernClosed == "" and _tavern_is_in_room("sandra", "TavernMain")

    def tavern_main_melissa_visible():
        return TavernClosed == "" and _tavern_is_in_room("melissa", "TavernMain")

    def tavern_main_amanda_visible():
        return TavernClosed == "" and _tavern_is_in_room("amanda", "TavernMain")

    def tavern_main_georgett_visible():
        return TavernClosed == "" and GeorgettAvail == 1

    def tavern_main_liza_visible():
        return TavernClosed == "" and LizaAvail == 1

    def tavern_main_clara_visible():
        return TavernClosed == "" and clara_visible_in_location("TavernMain")

    def tavern_main_becky_visible():
        return TavernClosed == "" and _tavern_is_in_room("becky", "TavernMain")

    def tavern_main_werecat_visible():
        return TavernClosed == "" and werecat_npc_present("TavernMain")

    def tavern_main_morning_routine_text():
        routine_pool = [
            "Сандра уже успела открыть ставни и теперь гоняет домашних, чтобы к полудню все выглядело прилично. Мелисса протирает столы, а Аманда то носит кувшины, то отвлекается на болтовню.",
            "Утренней суеты пока куда больше, чем настоящей работы: кто-то перетаскивает кувшины, кто-то вытряхивает тряпки, а Сандра с привычной строгостью следит, чтобы все не ленились.",
            "До настоящего наплыва гостей еще есть время, и потому в зале царит домашняя возня: столы выправляют, лавки двигают, а между делом успевают перекинуться парой слов и даже посмеяться.",
        ]
        if len(routine_pool) <= 0:
            return ""
        try:
            routine_index = int((dayspassed or 0) + (day or 0) + (month or 0)) % len(routine_pool)
        except Exception:
            routine_index = 0
        return str(routine_pool[routine_index] or "")

    def tavern_main_preopening_background():
        return str(tavern_main_morning_event_data().get("picture", "") or "images/tavern/mainhall/main_hall.png")

    def tavern_main_morning_event_text():
        return str(tavern_main_morning_event_data().get("text", "") or "")

    def tavern_main_build_description():
        if str(TavernEventOngoing or "").strip():
            return str(TavernEventOngoing or "")

        base_desc = str(TavernMainRoom.descriptions[0].text or "")
        desc_parts = [base_desc]

        if str(TavernClosed or "").strip():
            desc_parts.append(str(TavernClosed or ""))
        else:
            if tavern_preopening_mode():
                desc_parts.append("Утро в трактире еще не перешло в обычный рабочий ритм. До полудня вы и ваши домочадцы только готовите зал, кухню и припасы к дневной суете.")
                desc_parts.append(tavern_main_morning_routine_text())
                desc_parts.append(tavern_main_morning_event_text())
                desc_parts.append("На кухне с утра возятся: " + str(tavern_household_present_names("TavernKitchen") or "никто") + ".")
                desc_parts.append("В зале сейчас видны: " + str(tavern_household_present_names("TavernMain") or "никто") + ".")
                desc_parts.append("По двору и кладовым шныряют: " + str(_tavern_join_names([name for name in ("sandra", "melissa", "amanda") if _tavern_is_in_room(name, "Backyard") or _tavern_is_in_room(name, "TavernStorage")]) or "никто") + ".")
                desc_parts.append("Сейчас как раз удобное время перекинуться с домашними парой слов, прежде чем начнется обычная работа.")
            else:
                desc_parts.append("На кухне в вашем трактире работают: " + str(NamesList("jobkitchen", "TavernKitchen") or "никто") + ".")
                desc_parts.append("За чистоту и порядок отвечают: " + str(NamesList("jobcleaning", "TavernMain") or "никто") + ".")
                desc_parts.append("Еду и выпивку пьяным, трезвым, похотливым, скромным и прочим посетителям разносят: " + str(NamesList("jobwaitress", "TavernMain") or "никто") + ".")
                desc_parts.append("Вы можете пообщаться с участницами своей команды через список персонажей справа.")

            if clara_visible_in_location("TavernMain"):
                desc_parts.append("Кларисса снова заглянула в трактир и, похоже, в последнее время заметно сдружилась с Мелиссой: обе держатся рядом, перешептываются между столами и временами вместе прыскают со смеху.")
            if _tavern_is_in_room("becky", "TavernMain"):
                desc_parts.append("Бекки Блэнкеншип на этот раз сама заглянула к вам в трактир и присматривается к залу цепким хозяйским взглядом.")
            if str(TavernMainExtraDesc or "").strip():
                desc_parts.append(str(TavernMainExtraDesc or ""))
            if str(TavernMainGloryDesc or "").strip():
                desc_parts.append(str(TavernMainGloryDesc or ""))

        return "\n\n".join([part for part in desc_parts if str(part or "").strip()])

    TavernMainRoom = Room(
        code_name="TavernMain",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Главная зала трактира",
        bg_picture="bg TavernMain",
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
        npcs=[
            {"npc_id": "sandra", "name": "Сандра", "condition": tavern_main_sandra_visible, "talk_label": "IntSandraTalk", "auto_card": True},
            {"npc_id": "melissa", "name": "Мелисса", "condition": tavern_main_melissa_visible, "talk_label": "IntMelissaTalk", "auto_card": True},
            {"npc_id": "amanda", "name": "Аманда", "condition": tavern_main_amanda_visible, "talk_label": "IntAmandaTalk", "auto_card": True},
            {"npc_id": "georgett", "name": "Жоржетта", "condition": tavern_main_georgett_visible, "talk_label": "IntGeorgettTalk", "talk_args": ("georgett", "tavern"), "auto_card": True},
            {"npc_id": "liza", "name": "Лизетта", "condition": tavern_main_liza_visible, "talk_label": "IntLizaTalk", "auto_card": True},
            {"npc_id": "clara", "name": "Кларисса", "condition": tavern_main_clara_visible, "talk_label": "IntClaraTalk", "auto_card": True},
            {"npc_id": "becky", "name": "Бекки", "condition": tavern_main_becky_visible, "talk_label": "IntBeckyTalk", "auto_card": True},
            {"npc_id": "werecat", "name": "Луна", "condition": tavern_main_werecat_visible, "talk_label": "IntWerecatTalk", "auto_card": True},
        ],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "hall_staff_jobs": ["jobkitchen", "jobcleaning", "jobwaitress"],
            "object_menu_label": "TavernMainObjectMenu",
        },
    )

default TavernMainBlockEvents = 0
default TavernMainObjectMenuId = ""

label TavernMain:
    $ _tavern_main_base_desc = TavernMainRoom.descriptions[0].text
    $ MainTxt = _tavern_main_base_desc
    $ CurLocDesc = _tavern_main_base_desc
    scene black
    show bg TavernMain at master
    $ CurrentRoom = TavernMainRoom
    $ CurLoc = "TavernMain"
    $ location = CurLoc
    $ tavern_main_fireplace_wood_stock()
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    if tavern_preopening_mode():
        $ _layout_last_picture = tavern_main_preopening_background()
    $ CurrentRoom = TavernMainRoom
    $ current_action_items = []
    #$ current_action_title = "Действия в трактире"####### OLD CODE 
    #$ current_action_content = None
    #$ current_action_items = []
    $ current_girl_key = ""
    #$ current_object_id = ""
    python:
        # Force TavernMain base intro text in the left panel; prevents stale/conditional text bleed.
        _glory_quest_started = 0
        try:
            _dv = DraupnirVar
        except NameError:
            _dv = {}
        if isinstance(_dv, dict):
            _glory_quest_started = int(_dv.get("GloryHoleAsked", 0) or 0)
        try:
            _cur_desc_low = str(CurLocDesc or "").lower()
        except NameError:
            _cur_desc_low = ""
        if ("глорихол" in _cur_desc_low) and _glory_quest_started <= 0:
            MainTxt = _tavern_main_base_desc
            CurLocDesc = _tavern_main_base_desc
    

    # Startup safety: no Glory Hole stage before the quest/dialog branch starts.
    if int(week or 1) == 1 and int(day or 1) == 1:
        if int(DraupnirVar.get("GloryHoleAsked", 0) or 0) == 0:
            $ TavernGloryHole = 0
            $ TavernHole = 0
    # Determine if tavern is closed
    $ TavernClosed = ""
    if week == 7 and time < 3:
        $ TavernClosed = "Сейчас трактир закрыт, все ушли на службу в храм. Может вам тоже стоит пойти?"
    elif week == 5 and time == 3:
        $ TavernClosed = "Сейчас трактир закрыт, все ушли пятничное общегородское празднование. Может вам тоже стоит пойти?"
    elif time > 3:
        $ TavernClosed = "Сейчас поздняя ночь и трактир закрыт, все спят. Ну а кто не спит - тот отдыхает. Но не в главной зале."
    else:
        python:
            _arg_list = _args or ()
            BlockEvents = _arg_list[0] if len(_arg_list) > 0 else TavernMainBlockEvents
            TavernMainBlockEvents = 0
            TavernEventOngoing = ""
            TavernMainExtraDesc = ""
            TavernMainGloryDesc = ""
            ShouldDispatchTavernEvent = (
                int(week or 0) != 7
                and not tavern_preopening_mode()
                and (
                    int(EventsCount.get(10, 0) or 0) > 0
                    or (
                        int(BlockEvents or 0) != 1
                        and renpy.random.randint(1, 2) == 1
                        and int(EventsCount.get(time, 0) or 0) > 0
                    )
                )
            )

        if ShouldDispatchTavernEvent:
            call DisplayTavernEventShort(time, 1)
            $ TavernEventOngoing = _return
    
    $ GirlNameTS1 = "georgett"
    $ GirlNameTS2 = "liza"
    $ kitchenlist = NamesList("jobkitchen", "TavernKitchen")
    $ cleaninglist = NamesList("jobcleaning", "TavernMain")
    $ waitresslist = NamesList("jobwaitress", "TavernMain")

    if navigation_only_mode_enabled():
        if not tavern_preopening_mode():
            call TavernShowImage
        else:
            $ _layout_last_picture = tavern_main_preopening_background()
        python:
            _nav_desc_parts = [
                _tavern_main_base_desc,
                navigation_only_message(),
                navigation_only_time_note(),
            ]
            CurLocDesc = "\n\n".join([part for part in _nav_desc_parts if str(part or "").strip()])
            MainTxt = CurLocDesc
        $ renpy.pause(hard=True)
        jump TavernMain

    # Main event and interaction logic
    if TavernEventOngoing == "" and TavernClosed == "":
        if CurrentLoc[GirlNameTS1] == CurLoc and time > 2:
            if time == 3:
                call AddOthersSperm(GirlNameTS1, 7)
                call AddOthersSperm(GirlNameTS2, 8)
            if jobwhore["liza"] == 1 and jobwhore["georgett"] == 1:
                python:
                    randvarPS = renpy.random.randint(1, 5)
                if randvarPS == 1 and dyneval(CheckIfSexEventExist, GirlNameTS1, time) > 0:
                    $ TavernMainExtraDesc = "В правом углу трактира сидит юная Лизетта и ждет клиентов. А вот ее мамаша клиента уже похоже нашла."
                    $ LizaAvail = 1
                elif randvarPS == 2 and dyneval(CheckIfSexEventExist, GirlNameTS2, time) > 0:
                    $ TavernMainExtraDesc = "В правом углу трактира сидит Жоржетта и ждет клиентов. А вот ее старшую дочку, судя по всему, уже кто-то снял."
                    $ GeorgettAvail = 1
                else:
                    $ TavernMainExtraDesc = "В правом углу трактира сидят Жоржетта со своей дочкой Лизеттой и ждут клиентов."
                    $ LizaAvail = 1
                    $ GeorgettAvail = 1
            elif jobwhore["liza"] == 1:
                python:
                    randvarPS = renpy.random.randint(1, 3)
                if randvarPS == 1 and dyneval(CheckIfSexEventExist, GirlNameTS2, time) > 0:
                    $ TavernMainExtraDesc = "В правом углу, где обычно сидит Лизетта, пусто. Похоже что ветренную девчонку уже кто-то снял."
                else:
                    $ TavernMainExtraDesc = "В правом углу трактира сидит Лизетта и ждет клиентов."
                    $ LizaAvail = 1
            elif jobwhore["georgett"] == 1:
                python:
                    randvarPS = renpy.random.randint(1, 3)
                if randvarPS == 1 and dyneval(CheckIfSexEventExist, GirlNameTS1, time) > 0:
                    $ TavernMainExtraDesc = "В правом углу, где обычно сидит Жоржетта, пусто. Похоже что шлюшку уже кто-то снял."
                else:
                    $ TavernMainExtraDesc = "В правом углу трактира сидит Жоржетта и ждет клиентов."
                    $ GeorgettAvail = 1
        $ _glory_quest_started = int(DraupnirVar.get("GloryHoleAsked", 0) or 0) > 0
        if TavernGloryHole == 1 and _glory_quest_started:
            $ TavernMainGloryDesc = "В дальнем углу трактира мастера Драупнир что-то строгает и пилит. Работа кипит. Еще несколько часов и вы сможете насладиться построенным глорихолом."
        elif TavernGloryHole == 2 and _glory_quest_started:
            $ TavernMainGloryDesc = "В дальнем углу трактира располагается ширмочка, а за ней, как вы знаете, глорихол - место где, за умеренную плату, а для вас, как вы надеетесь, и вовсе бесплатно, любой страждущий может получить полностью анонимный минет. Ну, если с другой стороны ширмы есть кто-то, желающий его сделать."
        call TavernShowImage

    if TavernEventOngoing == "":
        call CheckDailyEvent("", "_story_enter", CurLoc, time)
        if TavernClosed == "" and not tavern_preopening_mode() and int(week or 0) != 7:
            call CheckDailyEvent('amanda')
            call CheckDailyEvent('sandra')
            call CheckDailyEvent('melissa')
            $ _tmp_bf_sandra = DescribeBreastFeeding('sandra')
            $ _tmp_bf_amanda = DescribeBreastFeeding('amanda')
            $ _tmp_bf_melissa = DescribeBreastFeeding('melissa')
            if GeorgettAvail == 1:
                $ _tmp_bf_georgett = DescribeBreastFeeding('georgett')
            if LizaAvail == 1:
                $ _tmp_bf_liza = DescribeBreastFeeding('liza')
            if CurrentLoc['georgett'] == 'TavernMain':
                $ _tmp_kids_list = ShowFullKidsListByAge('sandra','amanda','melissa','georgett','liza')
            else:
                $ _tmp_kids_list = ShowFullKidsListByAge('sandra','amanda','melissa')
            if GeorgettAvail == 1 or (CurrentLoc['georgett'] == CurLoc and time < 2):
                call CheckDailyEvent('georgett')
            if LizaAvail == 1 or (CurrentLoc['liza'] == CurLoc and time < 2):
                call CheckDailyEvent('liza')
        call TavernMainBuildActions
        
    else:
        $ CurLocDesc = TavernEventOngoing
        $ MainTxt = TavernEventOngoing
        $ current_action_title = "Ваши действия"
        $ current_action_content = None

    if TavernEventOngoing == "":
        $ CurLocDesc = tavern_main_build_description()
        $ MainTxt = CurLocDesc

    if TavernEventOngoing == "" and TavernClosed == "":
        if amanda_revealing_dress_request_ready() and _tavern_is_in_room("amanda", "TavernMain"):
            call AmandaDressRequestEvent
        elif melissa_revealing_dress_request_ready() and _tavern_is_in_room("melissa", "TavernMain"):
            call MelissaDressRequestEvent
        else:
            python:
                _household_request_type, _household_request_girl = household_pending_request_girl("TavernMain")
            if str(_household_request_type or "") == "soap":
                call HouseholdSoapRequestEvent(_household_request_girl)

    jump TavernMainView


label TavernMainView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernMainView


label TavernMainBuildActions:
    $ tavern_main_fireplace_wood_stock()
    $ current_action_title = "Действия в трактире"
    $ current_action_content = None
    $ _tavern_room_menu = CurrentRoom.build_menu_sections() if CurrentRoom is not None and hasattr(CurrentRoom, "build_menu_sections") else {"movement": [], "actions": []}
    $ current_action_items = list(_tavern_room_menu.get("movement", [])) + list(_tavern_room_menu.get("actions", []))
    if TavernClosed == "" and not tavern_preopening_mode() and story_event_available("TavernMain", "overheard"):
        $ current_action_items.append(MenuItem("Подслушать разговор в зале", Call("checkTriggers", "TavernMain", "overheard", 0)))
    return


label TavernMainObjectMenu(object_id="", refresh_only=False):
    $ tavern_main_fireplace_wood_stock()
    if str(object_id or "") != "":
        $ TavernMainObjectMenuId = object_id
    else:
        $ TavernMainObjectMenuId = current_object_id
    $ object_id = TavernMainObjectMenuId
    $ _tavern_object = None
    python:
        _tavern_room = CurrentRoom if CurrentRoom is not None else TavernMainRoom
        for _room_object in _tavern_room.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _tavern_object = _room_object
                break

    if _tavern_object is None:
        call TavernMainRestore
        return

    $ current_object_id = object_id
    $ current_action_title = str(_tavern_object.name or "Действия")
    $ current_action_content = None
    $ current_action_items = []  # Original
    if str(getattr(_tavern_object, "picture", "") or "").strip() and renpy.loadable(str(getattr(_tavern_object, "picture", "") or "").strip()):
        $ _layout_last_picture = str(getattr(_tavern_object, "picture", "") or "").strip()
    if str(object_id or "") == "fireplace_001":
        $ MainTxt = tavern_main_fireplace_description()
    else:
        $ MainTxt = str(_tavern_object.description or "")
    $ CurLocDesc = MainTxt

    python:
        for _tavern_action in _tavern_object.visible_actions():
            _tavern_args = tuple(getattr(_tavern_action, "args", ()) or ())
            if _tavern_action.hook == "text":
                current_action_items.append(MenuItem(_tavern_action.label, Call("TavernMainObjectText", object_id, _tavern_action.action_id)))
            elif _tavern_action.hook == "call" and str(_tavern_action.target or "") != "":
                current_action_items.append(MenuItem(_tavern_action.label, Call(_tavern_action.target, *_tavern_args)))
            elif _tavern_action.hook == "jump" and str(_tavern_action.target or "") != "":
                current_action_items.append(MenuItem(_tavern_action.label, Jump(_tavern_action.target)))
        current_action_items.append(MenuItem("Назад", Call("TavernMainRestore")))
    return


label TavernMainObjectText(object_id="", action_id=""):
    python:
        _tavern_text = ""
        _tavern_name = ""
        _tavern_room = CurrentRoom if CurrentRoom is not None else TavernMainRoom
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
            MainTxt = _tavern_text
            CurLocDesc = _tavern_text
            current_action_title = _tavern_name or "Действия"
    call TavernMainObjectMenu(object_id)
    return


label TavernMainRestore:
    $ scene_image = CurrentRoom.bg_picture or None
    if tavern_preopening_mode():
        $ _layout_last_picture = tavern_main_preopening_background()
    elif scene_image:
        $ _layout_last_picture = scene_image
    $ MainTxt = tavern_main_build_description()
    $ CurLocDesc = MainTxt
    call TavernMainBuildActions
    return
