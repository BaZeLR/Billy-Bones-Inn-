# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# PortStreets location - converted from legacy script
default PortStreetsBottleSpawnDay = -1
default PortStreetsBottlePresent = 0
default georgett_can_talk = 0
default liza_can_talk = 0

init python:
    import random

    def port_streets_georgett_can_talk():
        try:
            return int(georgett_can_talk or 0) == 1
        except Exception:
            return False

    def port_streets_liza_can_talk():
        try:
            return int(liza_can_talk or 0) == 1
        except Exception:
            return False

    def port_streets_prepare_bottle_spawn():
        global PortStreetsBottleSpawnDay
        global PortStreetsBottlePresent
        current_day = int(dayspassed or 0)
        if int(PortStreetsBottleSpawnDay or -1) == current_day:
            return
        PortStreetsBottleSpawnDay = current_day
        PortStreetsBottlePresent = 1 if random.randint(1, 3) == 1 else 0

    def port_streets_empty_bottle_visible():
        return int(PortStreetsBottlePresent or 0) == 1

    PortStreetsRoom = Room(
        code_name="PortStreets",
        group_name=ROOM_GROUP_CITY,
        display_name="Портовые переулки",
        bg_picture="images/georgett/Port/port1.jpg",
        descriptions=[
            RoomDescription(
                text="Вы находитесь в лабиринте узких улочек и переулков, ведущих к порту.\nГде-то здесь расположен храм богини Эллоны.",
                priority=200,
            ),
        ],
        exits=[
            RoomExit(label="Идти в храм Эллоны", target="EllonaTemple"),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[
            GameObject(
                object_id="port_lanes",
                name="Портовые переулки",
                description="Узкие переулки, ведущие к порту и скрывающие немало темных уголков.",
                actions=[
                    ObjectAction(
                        action_id="examine_port_lanes",
                        label="Осмотреть переулки",
                        hook="call",
                        target="PortStreetsExamineLanes",
                    ),
                ],
            ),
            GameObject(
                object_id="temple_route",
                name="Дорога к храму Эллоны",
                description="Где-то здесь между домами расположен небольшой храм Эллоны.",
                actions=[
                    ObjectAction(
                        action_id="go_temple",
                        label="Идти в храм Эллоны",
                        hook="jump",
                        target="EllonaTemple",
                    ),
                ],
            ),
            GameObject(
                object_id="port_empty_bottle",
                name="Пустая бутылка",
                description="Возле стены валяется пустая бутылка, будто ее недавно бросили мимо груды мусора.",
                actions=[
                    ObjectAction(
                        action_id="take_empty_bottle",
                        label="Подобрать бутылку",
                        hook="call",
                        target="PortStreetsTakeEmptyBottle",
                    ),
                    ObjectAction(
                        action_id="examine_empty_bottle",
                        label="Осмотреть бутылку",
                        hook="text",
                        target="Обычная пустая стеклянная бутылка. Если ее отмыть, она еще вполне пригодится в хозяйстве.",
                    ),
                ],
                condition=port_streets_empty_bottle_visible,
            ),
        ],
        schedule=RoomSchedule(
            [1, 2, 3, 4, 5, 6, 7],
            [],
            "",
            None,
            "00:00",
            "23:59",
        ),
        custom_properties={
            "street_prostitution_location": True,
        },
    )

label PortStreets:
    scene black
    call EnterLocation("PortStreets")
    $ dog_prepare_current_spawn()
    $ port_streets_prepare_bottle_spawn()
    $ CurrentRoom = PortStreetsRoom
    $ CurLoc = "PortStreets"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
        call ShowImage("", "", scene_image)
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    $ georgett_can_talk = 0
    $ liza_can_talk = 0

    if navigation_only_mode_enabled():
        python:
            _port_nav_parts = [
                PortStreetsRoom.descriptions[0].text,
                navigation_only_message(),
                navigation_only_time_note(),
            ]
            CurLocDesc = "\n\n".join([part for part in _port_nav_parts if str(part or "").strip()])
            MainTxt = CurLocDesc
            current_action_items = []
            for _port_exit in PortStreetsRoom.visible_exits():
                current_action_items.append(MenuItem(_port_exit.label, Jump(_port_exit.target)))
        $ _port_nav_ui_return = None
        while _port_nav_ui_return is None:
            call screen main_ui
            $ _port_nav_ui_return = _return
        jump PortStreets

    call RoomEnterEventGate(CurLoc, False)
    $ Georgett.sync_from_georgett_maps()
    $ Liza.sync_from_shared_state()

    $ GirlNamePS1 = "georgett"
    $ GirlNamePS2 = "liza"
    $ _port_street_clients_target = ""
    $ _port_street_clients_girl = ""
    $ _port_street_clients_extra = []
    $ _port_georgett_event_available = Georgett.portstreet_client_event_available()
    $ _port_liza_event_available = Liza.portstreet_client_event_available()
    $ _port_georgett_scheduled_here = Georgett.portstreet_work_active()
    $ _port_liza_scheduled_here = Liza.portstreet_work_active()
    $ _port_work_active = _port_georgett_scheduled_here or _port_liza_scheduled_here or _port_georgett_event_available or _port_liza_event_available

    # Main street logic.
    if _port_work_active and Georgett.portstreet_story_unblocked():
        if Friends.get(GirlNamePS1, 0) == 0:
            $ CurLocDesc = "На углу стоит {b}молодая женщина{/b}, не очень высокого роста, чуть пухленькая и с большой налитой грудью, одетая в прозрачную блузку и короткую юбку. Она белокура и кареглаза. Ее внешность и повадки не дают никаких сомнений в том, что она выбрала себе путь отнюдь не монашки."
            if pregnancy.get(GirlNamePS1, 0) >= 210:
                $ CurLocDesc += "\n\nОна беременна и находится на позднем сроке. Ее живот красноречиво об этом свидетельствует."
            if pregnancy.get(GirlNamePS1, 0) < 210 and pregnancy.get(GirlNamePS1, 0) >= 150:
                $ CurLocDesc += "\n\nСредних размеров беременный животик сексуально напоминает о ее бурной личной жизни."
            if pregnancy.get(GirlNamePS1, 0) > 120 and pregnancy.get(GirlNamePS1, 0) < 150:
                $ CurLocDesc += "\n\nВидно что она нагуляла себе животик, но он еще не очень заметен."
            $ MainTxt = CurLocDesc
            call ShowImage("georgett", "port", "wait")
            $ georgett_can_talk = 1
            $ liza_can_talk = 0
        else:
            call AddOthersSperm(GirlNamePS1, 6)

            if Liza.can_work_portstreets():
                call AddOthersSperm(GirlNamePS2, 8)
                $ randvarPS = renpy.random.randint(1, 5)
                if _port_georgett_event_available and _port_liza_event_available:
                    $ CurLocDesc = "На обычном углу Жоржетты и Лизетты сейчас пусто. Судя по тихим звукам из соседних подворотен, обе уже нашли клиентов."
                    $ MainTxt = CurLocDesc
                    $ georgett_can_talk = 0
                    $ liza_can_talk = 0
                    $ _port_street_clients_target = "Проверить подворотню Жоржетты"
                    $ _port_street_clients_girl = "georgett"
                    $ _port_street_clients_extra = [("Проверить подворотню Лизетты", "liza")]
                elif _port_georgett_event_available:
                    $ CurLocDesc = "На углу стоит юная Лизетта и ждет клиентов. А вот ее мамаша клиента уже похоже нашла."
                    $ MainTxt = CurLocDesc
                    $ georgett_can_talk = 0
                    $ liza_can_talk = 1
                    $ _port_street_clients_target = "Пойти проверить подворотню"
                    $ _port_street_clients_girl = "georgett"
                elif _port_liza_event_available:
                    $ CurLocDesc = "На углу стоит {b}Жоржетта{/b} и ждет клиентов. А вот ее старшую дочку, судя по всему, уже кто-то снял."
                    $ MainTxt = CurLocDesc
                    call ShowImage("georgett", "port", "lizaminet")
                    $ georgett_can_talk = 1
                    $ liza_can_talk = 0
                    $ _port_street_clients_target = "Пойти проверить подворотню"
                    $ _port_street_clients_girl = "liza"
                else:
                    $ CurLocDesc = "На углу стоит {b}Жоржетта{/b} со своей дочкой Лизеттой и ждут клиентов."
                    $ MainTxt = CurLocDesc
                    $ georgett_can_talk = 1
                    $ liza_can_talk = 1
            else:
                if _port_georgett_event_available or renpy.random.randint(1, 3) == 1:
                    $ CurLocDesc = "Почему-то Жоржетты сейчас нет на ее обычном месте. Где же она может быть?"
                    $ MainTxt = CurLocDesc
                    $ georgett_can_talk = 0
                    $ liza_can_talk = 0
                    if HadSex.get(GirlNamePS1, 0) > 0 or _port_georgett_event_available:
                        $ _port_street_clients_target = "Пойти проверить подворотню"
                        $ _port_street_clients_girl = "georgett"
                else:
                    $ CurLocDesc = "На углу стоит {b}Жоржетта{/b} и ждет клиентов."
                    $ MainTxt = CurLocDesc
                    call ShowImage("georgett", "port", "wait")
                    $ georgett_can_talk = 1
                    $ liza_can_talk = 0
    else:
        if int(clock_minutes or 0) < (13 * 60):
            $ _port_temple_road_pics = ["images/ellona/toTemple.png", "images/ellona/toTemple1.png"]
            $ _port_temple_road_pic = _port_temple_road_pics[renpy.random.randint(0, len(_port_temple_road_pics) - 1)]
            call ShowImage("", "", _port_temple_road_pic)
        else:
            call ShowImageSeq("georgett", "port", "port", 3)
        $ georgett_can_talk = 0
        $ liza_can_talk = 0
        $ CurLocDesc = PortStreetsRoom.descriptions[0].text
        if int(clock_minutes or 0) < (13 * 60):
            $ CurLocDesc += "\n\nНа дороге к храму Эллоны встречаются беременные женщины: кто-то идет за благословением, кто-то уже почти у самых дверей родильной."
        $ MainTxt = CurLocDesc

    if dog_is_here("PortStreets"):
        $ MainTxt += "\n\nВ тени стены крутится бродячий пес, настороженно поглядывающий на прохожих."
        $ CurLocDesc = MainTxt

    call PortStreetsBuildActions
    $ PortStreetsRoom.mark_visited()
    $ _port_ui_return = None
    while _port_ui_return is None:
        call screen main_ui
        $ _port_ui_return = _return
    jump PortStreets


label PortStreetsBuildActions:
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _port_object in PortStreetsRoom.visible_objects():
            current_action_items.append(MenuItem(_port_object.name, Call("PortStreetsObjectMenu", _port_object.object_id)))

    if _port_street_clients_target != "" and _port_street_clients_girl != "":
        $ _port_clients_action = "street_clients_liza" if _port_street_clients_girl == "liza" else "street_clients_georgett"
        $ current_action_items.append(MenuItem(_port_street_clients_target, Call("checkTriggers", "PortStreets", _port_clients_action, 0)))
    python:
        for _port_extra_label, _port_extra_girl in list(_port_street_clients_extra or []):
            if str(_port_extra_label or "").strip() and str(_port_extra_girl or "").strip():
                _port_clients_action = "street_clients_liza" if str(_port_extra_girl) == "liza" else "street_clients_georgett"
                current_action_items.append(MenuItem(str(_port_extra_label), Call("checkTriggers", "PortStreets", _port_clients_action, 0)))

    python:
        for _port_exit in PortStreetsRoom.visible_exits():
            current_action_items.append(MenuItem(_port_exit.label, Jump(_port_exit.target)))

    return


label PortStreetsObjectMenu(object_id=""):
    $ _port_object = None
    python:
        for _room_object in PortStreetsRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _port_object = _room_object
                break

    if _port_object is None:
        call PortStreetsBuildActions
        return

    $ current_action_title = _port_object.name
    $ current_action_content = None
    $ current_action_items = []

    python:
        for _port_action in _port_object.visible_actions():
            if _port_action.hook == "text":
                current_action_items.append(MenuItem(_port_action.label, Call("PortStreetsObjectText", object_id, _port_action.action_id)))
            elif _port_action.hook == "call" and str(_port_action.target or "") != "":
                _port_args = tuple(getattr(_port_action, "args", ()) or ())
                current_action_items.append(MenuItem(_port_action.label, Call(_port_action.target, *_port_args)))
            elif _port_action.hook == "jump" and str(_port_action.target or "") != "":
                current_action_items.append(MenuItem(_port_action.label, Jump(_port_action.target)))

    $ current_action_items.append(MenuItem("Назад", Call("PortStreetsBuildActions")))
    return


label PortStreetsObjectText(object_id="", action_id=""):
    python:
        _port_text = ""
        for _room_object in PortStreetsRoom.visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _port_text = str(_room_action.target or "")
                    break
            break
        if _port_text:
            MainTxt = _port_text
            CurLocDesc = _port_text
    call PortStreetsObjectMenu(object_id)
    return


label PortStreetsExamineLanes:
    scene black
    $ _port_lanes_pictures = ["images/general/port_streets.png", "images/general/port_streets1.png", "images/general/port_streets2.png", "images/general/port_streets4.png", "images/general/port_streets5.png"]
    $ _port_lanes_picture = _port_lanes_pictures[renpy.random.randint(0, len(_port_lanes_pictures) - 1)]
    $ scene_image = _port_lanes_picture
    $ _layout_last_picture = _port_lanes_picture
    $ MainTxt = "В этих темных углах любой искатель приключений может найти острые ощущения, которые удовлетворят его вкусы, а при неудаче, возможно, и его смерть."
    $ CurLocDesc = MainTxt
    call PortStreetsObjectMenu("port_lanes")
    return


label PortStreetsTakeEmptyBottle:
    if int(PortStreetsBottlePresent or 0) != 1:
        call PortStreetsBuildActions
        return
    $ PortStreetsBottlePresent = 0
    $ _player_add_item_by_id("empty_bottle_001", 1)
    $ MainTxt = "Вы подбираете пустую бутылку. Стекло цело, и если ее как следует отмыть, она еще пригодится."
    $ CurLocDesc = MainTxt
    call PortStreetsBuildActions
    return
