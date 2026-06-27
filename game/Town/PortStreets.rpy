# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# PortStreets location - converted from legacy script

init python:
    def port_streets_georgett_can_talk():
        return Georgett.portstreet_visible_now()

    def port_streets_liza_can_talk():
        return Liza.portstreet_visible_now()

    def port_streets_prepare_bottle_spawn():
        current_day = int(dayspassed or 0)
        if int(PortStreetsRoom.custom_properties.get("bottle_spawn_day", -1) or -1) == current_day:
            return
        PortStreetsRoom.custom_properties["bottle_spawn_day"] = current_day
        PortStreetsRoom.custom_properties["bottle_present"] = 1 if procedural_randint(1, 3, key="procedural:Town/PortStreets.rpy:procedural_randint:18:1") == 1 else 0

    def port_streets_empty_bottle_visible():
        return int(PortStreetsRoom.custom_properties.get("bottle_present", 0) or 0) == 1

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
                object_id="port_empty_bottle",
                name="Пустая бутылка",
                description="Возле стены валяется пустая бутылка, будто ее недавно бросили мимо груды мусора.",
                actions=[
                    ObjectAction(
                        action_id="examine_empty_bottle",
                        label="Осмотреть бутылку",
                        hook="call",
                        target="PortStreetsExamineEmptyBottle",
                    ),
                    ObjectAction(
                        action_id="take_empty_bottle",
                        label="Подобрать бутылку",
                        hook="call",
                        target="PortStreetsTakeEmptyBottle",
                    ),
                ],
                condition=port_streets_empty_bottle_visible,
                custom_properties={"object_menu_label": "PortStreetsBottleMenu"},
            ),
        ],
        action_menus=[
            RoomAction(
                action_id="examine_port_lanes",
                label="Осмотреть переулки",
                hook="call",
                target="PortStreetsExamineLanes",
            ),
        ],
        schedule=None,
        custom_properties={
            "street_prostitution_location": True,
            "bottle_spawn_day": -1,
            "bottle_present": 0,
        },
    )

label PortStreets:
    $ CurrentRoom = PortStreetsRoom
    $ CurLoc = CurrentRoom.code_name
    $ location = CurLoc
    call RoomEnterEventGate(CurLoc, False)
    $ dog_prepare_current_spawn()
    $ port_streets_prepare_bottle_spawn()
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
        vscene scene_image
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ Georgett.set_portstreet_visible(False)
    $ Liza.set_portstreet_visible(False)

    if navigation_only_mode_enabled():
        python:
            _port_nav_parts = [
                PortStreetsRoom.descriptions[0].text,
                navigation_only_message(),
                navigation_only_time_note(),
            ]
            CurLocDesc = "\n\n".join([part for part in _port_nav_parts if str(part or "").strip()])
            MainTxt = CurLocDesc
            current_action_items = CurrentRoom.build_exit_items()
        $ _port_nav_ui_return = None
        while _port_nav_ui_return is None:
            call screen main_ui
            $ _port_nav_ui_return = _return
        jump PortStreets

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
        if people_to_int(Georgett.rel, 0) == 0:
            $ CurLocDesc = "На углу стоит {b}молодая женщина{/b}, не очень высокого роста, чуть пухленькая и с большой налитой грудью, одетая в прозрачную блузку и короткую юбку. Она белокура и кареглаза. Ее внешность и повадки не дают никаких сомнений в том, что она выбрала себе путь отнюдь не монашки."
            if Georgett.pregnancy_days() >= 210:
                $ CurLocDesc += "\n\nОна беременна и находится на позднем сроке. Ее живот красноречиво об этом свидетельствует."
            if Georgett.pregnancy_days() < 210 and Georgett.pregnancy_days() >= 150:
                $ CurLocDesc += "\n\nСредних размеров беременный животик сексуально напоминает о ее бурной личной жизни."
            if Georgett.pregnancy_days() > 120 and Georgett.pregnancy_days() < 150:
                $ CurLocDesc += "\n\nВидно что она нагуляла себе животик, но он еще не очень заметен."
            $ MainTxt = CurLocDesc
            $ _georgett_port_picture = Georgett.portstreet_scene_picture()
            if str(_georgett_port_picture or "").strip():
                $ scene_image = _georgett_port_picture
                $ _layout_last_picture = scene_image
                vscene scene_image
            $ Georgett.set_portstreet_visible(True)
            $ Liza.set_portstreet_visible(False)
        else:
            call AddOthersSperm(GirlNamePS1, 6)

            if Liza.can_work_portstreets():
                call AddOthersSperm(GirlNamePS2, 8)
                $ randvarPS = procedural_randint(1, 5, key="procedural:Town/PortStreets.rpy:procedural_randint:158:2")
                if _port_georgett_event_available and _port_liza_event_available:
                    $ CurLocDesc = "На обычном углу Жоржетты и Лизетты сейчас пусто. Судя по тихим звукам из соседних подворотен, обе уже нашли клиентов."
                    $ MainTxt = CurLocDesc
                    $ Georgett.set_portstreet_visible(False)
                    $ Liza.set_portstreet_visible(False)
                    $ _port_street_clients_target = "Проверить подворотню Жоржетты"
                    $ _port_street_clients_girl = "georgett"
                    $ _port_street_clients_extra = [("Проверить подворотню Лизетты", "liza")]
                elif _port_georgett_event_available:
                    $ CurLocDesc = "На углу стоит юная Лизетта и ждет клиентов. А вот ее мамаша клиента уже похоже нашла."
                    $ MainTxt = CurLocDesc
                    $ Georgett.set_portstreet_visible(False)
                    $ Liza.set_portstreet_visible(True)
                    $ _port_street_clients_target = "Пойти проверить подворотню"
                    $ _port_street_clients_girl = "georgett"
                elif _port_liza_event_available:
                    $ CurLocDesc = "На углу стоит {b}Жоржетта{/b} и ждет клиентов. А вот ее старшую дочку, судя по всему, уже кто-то снял."
                    $ MainTxt = CurLocDesc
                    call ShowImage("georgett", "port", "lizaminet")
                    $ Georgett.set_portstreet_visible(True)
                    $ Liza.set_portstreet_visible(False)
                    $ _port_street_clients_target = "Пойти проверить подворотню"
                    $ _port_street_clients_girl = "liza"
                else:
                    $ CurLocDesc = "На углу стоит {b}Жоржетта{/b} со своей дочкой Лизеттой и ждут клиентов."
                    $ MainTxt = CurLocDesc
                    $ Georgett.set_portstreet_visible(True)
                    $ Liza.set_portstreet_visible(True)
            else:
                if _port_georgett_event_available or procedural_randint(1, 3, key="procedural:Town/PortStreets.rpy:procedural_randint:188:3") == 1:
                    $ CurLocDesc = "Почему-то Жоржетты сейчас нет на ее обычном месте. Где же она может быть?"
                    $ MainTxt = CurLocDesc
                    $ Georgett.set_portstreet_visible(False)
                    $ Liza.set_portstreet_visible(False)
                    if Georgett.had_sex_count() > 0 or _port_georgett_event_available:
                        $ _port_street_clients_target = "Пойти проверить подворотню"
                        $ _port_street_clients_girl = "georgett"
                else:
                    $ CurLocDesc = "На углу стоит {b}Жоржетта{/b} и ждет клиентов."
                    $ MainTxt = CurLocDesc
                    $ _georgett_port_picture = Georgett.portstreet_scene_picture()
                    if str(_georgett_port_picture or "").strip():
                        $ scene_image = _georgett_port_picture
                        $ _layout_last_picture = scene_image
                        vscene scene_image
                    $ Georgett.set_portstreet_visible(True)
                    $ Liza.set_portstreet_visible(False)
    else:
        if int(clock_minutes or 0) < (13 * 60):
            $ _port_temple_road_pics = ["images/ellona/toTemple.png", "images/ellona/toTemple1.png"]
            $ _port_temple_road_pic = _port_temple_road_pics[procedural_randint(0, len(_port_temple_road_pics) - 1, key="procedural:Town/PortStreets.rpy:procedural_randint:205:4")]
            vscene _port_temple_road_pic
        else:
            call ShowImageSeq("georgett", "port", "port", 3)
        $ Georgett.set_portstreet_visible(False)
        $ Liza.set_portstreet_visible(False)
        $ CurLocDesc = PortStreetsRoom.descriptions[0].text
        if int(clock_minutes or 0) < (13 * 60):
            $ CurLocDesc += "\n\nНа дороге к храму Эллоны встречаются беременные женщины: кто-то идет за благословением, кто-то уже почти у самых дверей родильной."
        $ MainTxt = CurLocDesc

    if dog_is_here("PortStreets"):
        $ MainTxt += "\n\nВ тени стены крутится бродячий пес, настороженно поглядывающий на прохожих."
        $ CurLocDesc = MainTxt

    python:
        current_action_items = CurrentRoom.build_action_items()
        if str(_port_street_clients_target or "") != "" and str(_port_street_clients_girl or "") != "":
            current_action_items.append(MenuItem(_port_street_clients_target, Call("PortStreetsBackAlley", _port_street_clients_girl)))
        for _port_extra_label, _port_extra_girl in list(_port_street_clients_extra or []):
            if str(_port_extra_label or "").strip() and str(_port_extra_girl or "").strip():
                current_action_items.append(MenuItem(str(_port_extra_label), Call("PortStreetsBackAlley", str(_port_extra_girl))))
        current_action_items.extend(CurrentRoom.build_exit_items())
    $ PortStreetsRoom.mark_visited()
    $ _port_ui_return = None
    while _port_ui_return is None:
        call screen main_ui
        $ _port_ui_return = _return
    jump PortStreets


label PortStreetsBackAlley(girl_name=""):
    $ CurrentRoom = PortStreetsRoom
    $ CurLoc = CurrentRoom.code_name
    $ location = CurLoc
    $ UI_mode = "scene"
    $ scene_image = "images/general/port_streets.png"
    if scene_image:
        $ _layout_last_picture = scene_image
        vscene scene_image
    if str(girl_name or "") == "":
        if Georgett.portstreet_client_event_available():
            $ girl_name = "georgett"
        elif Liza.portstreet_client_event_available():
            $ girl_name = "liza"
    $ current_action_title = "Подворотня"
    $ current_action_content = None
    if str(girl_name or "") == "liza":
        $ MainTxt = "Вы сворачиваете с портовой улицы в темную подворотню Лизетты. Из глубины уже доносятся приглушенные звуки."
    elif str(girl_name or "") == "georgett":
        $ MainTxt = "Вы сворачиваете с портовой улицы в знакомую подворотню Жоржетты. Из темноты доносится возня и приглушенные голоса."
    else:
        $ MainTxt = "Вы проверяете подворотню, но сегодня здесь пусто."
    $ CurLocDesc = MainTxt
    if str(girl_name or "") in ("georgett", "liza") and CheckIfSexEventExist(girl_name, 3, "Prostitution") > 0:
        $ current_action_items = [MenuItem("Подсмотреть", Call("street_clients_watch", 1, girl_name, time)), MenuItem("Вернуться в портовые переулки", Jump("PortStreets"))]
    else:
        $ current_action_items = [MenuItem("Вернуться в портовые переулки", Jump("PortStreets"))]
    call screen main_ui
    jump PortStreets


label PortStreetsBottleMenu(object_id="port_empty_bottle"):
    $ _port_bottle = None
    python:
        for _room_object in CurrentRoom.visible_objects():
            if getattr(_room_object, "object_id", "") == "port_empty_bottle":
                _port_bottle = _room_object
                break
    if _port_bottle is None:
        $ current_action_title = "Действия"
        $ current_action_items = CurrentRoom.build_action_items() + CurrentRoom.build_exit_items()
        return
    $ current_action_title = _port_bottle.name
    $ MainTxt = _port_bottle.description
    $ CurLocDesc = MainTxt
    python:
        current_action_items = []
        for _port_bottle_action in _port_bottle.visible_actions():
            if str(_port_bottle_action.hook or "") == "call" and str(_port_bottle_action.target or ""):
                current_action_items.append(MenuItem(_port_bottle_action.label, Call(_port_bottle_action.target)))
        current_action_items.append(MenuItem("Назад", Jump("PortStreets")))
    return


label PortStreetsExamineLanes:
    $ _port_lanes_pictures = ["images/general/port_streets.png", "images/general/port_streets1.png", "images/general/port_streets2.png", "images/general/port_streets4.png", "images/general/port_streets5.png"]
    $ _port_lanes_picture = _port_lanes_pictures[procedural_randint(0, len(_port_lanes_pictures) - 1, key="procedural:Town/PortStreets.rpy:procedural_randint:292:5")]
    $ scene_image = _port_lanes_picture
    $ _layout_last_picture = _port_lanes_picture
    vscene _port_lanes_picture
    $ MainTxt = "В этих темных углах любой искатель приключений может найти острые ощущения, которые удовлетворят его вкусы, а при неудаче, возможно, и его смерть."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Действия"
    $ current_action_items = CurrentRoom.build_action_items() + CurrentRoom.build_exit_items()
    return


label PortStreetsExamineEmptyBottle:
    $ MainTxt = "Обычная пустая стеклянная бутылка. Если ее отмыть, она еще вполне пригодится в хозяйстве."
    $ CurLocDesc = MainTxt
    call PortStreetsBottleMenu("port_empty_bottle")
    return


label PortStreetsTakeEmptyBottle:
    if not port_streets_empty_bottle_visible():
        $ current_action_items = CurrentRoom.build_action_items() + CurrentRoom.build_exit_items()
        return
    $ PortStreetsRoom.custom_properties["bottle_present"] = 0
    $ _player_add_item_by_id("empty_bottle_001", 1)
    $ MainTxt = "Вы подбираете пустую бутылку. Стекло цело, и если ее как следует отмыть, она еще пригодится."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Действия"
    $ current_action_items = CurrentRoom.build_action_items() + CurrentRoom.build_exit_items()
    return
