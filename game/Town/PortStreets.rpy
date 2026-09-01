# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# PortStreets location - converted from legacy script

init python:
    def port_streets_prepare_bottle_spawn():
        current_day = int(current_game_day())
        if int(rooms.get("PortStreets").custom_properties.get("bottle_spawn_day", -1) or -1) == current_day:
            return
        rooms.get("PortStreets").custom_properties["bottle_spawn_day"] = current_day
        rooms.get("PortStreets").custom_properties["bottle_present"] = 1 if procedural_randint(1, 3, key="procedural:Town/PortStreets.rpy:procedural_randint:18:1") == 1 else 0

    def port_streets_empty_bottle_visible():
        return int(rooms.get("PortStreets").custom_properties.get("bottle_present", 0) or 0) == 1

    def port_streets_client_event_available():
        return story_event_available("PortStreets", "street_clients") or port_streets_repeat_georgett_client_event_available()

    def port_streets_repeat_georgett_client_event_available():
        return int(Georgett.story_value("seeclients", 0) or 0) > 0 and Georgett.portstreet_client_event_available()

    def port_streets_examine_lanes_visible():
        return not port_streets_client_event_available()

    def port_streets_before_afternoon():
        return people_to_int(calendar_v2.hour, 0) < 13

    PortStreetsRoomDefinition = Room(
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
            RoomExit(label="Идти в храм Эллоны", target="EllonaTemple", minutes_to_pass=10),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern", minutes_to_pass=10),
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
                action_id="street_clients",
                label="Пойти проверить подворотню",
                hook="call",
                target="story_georgett_portstreet_clients",
                condition=port_streets_repeat_georgett_client_event_available,
            ),
            RoomAction(
                action_id="examine_port_lanes",
                label="Осмотреть переулки",
                hook="call",
                target="PortStreetsExamineLanes",
                condition=port_streets_examine_lanes_visible,
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
    $ renpy.dynamic("_port_temple_road_pics", "_port_temple_road_pic")
    $ rooms.enter("PortStreets")
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.talk_picture = ""
    $ main_ui_runtime.clear_contexts()
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""
    call RoomEnterEventGate(rooms.current_code, False)
    $ port_streets_prepare_bottle_spawn()
    $ scene_runtime.picture = rooms.current.bg_picture or None
    if scene_runtime.picture:
        vscene scene_runtime.picture
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []

    $ scene_runtime.location_text = rooms.get("PortStreets").descriptions[0].text
    if Georgett.portstreet_client_event_available():
        $ scene_runtime.location_text += "\n\nПочему-то Жоржетты сейчас нет на ее обычном месте. Где же она может быть?"
    elif Georgett.portstreet_visible_now() and people_to_int(Georgett.rel, 0) == 0:
        vscene "images/georgett/Port/wait.jpg"
        $ scene_runtime.location_text += "\n\nНа углу стоит молодая женщина, не очень высокого роста, чуть пухленькая и с большой налитой грудью, одетая в прозрачную блузку и короткую юбку. Она белокура и кареглаза. Ее внешность и повадки не дают никаких сомнений в том, что она выбрала себе путь отнюдь не монашки."
        if Georgett.pregnancy_days() >= 210:
            $ scene_runtime.location_text += "\n\nОна беременна и находится на позднем сроке. Ее живот красноречиво об этом свидетельствует."
        elif Georgett.pregnancy_days() >= 150:
            $ scene_runtime.location_text += "\n\nСредних размеров беременный животик сексуально напоминает о ее бурной личной жизни."
        elif Georgett.pregnancy_days() > 120:
            $ scene_runtime.location_text += "\n\nВидно что она нагуляла себе животик, но он еще не очень заметен."
    elif port_streets_before_afternoon():
        $ _port_temple_road_pics = ["images/ellona/toTemple.png", "images/ellona/toTemple1.png"]
        $ _port_temple_road_pic = _port_temple_road_pics[procedural_randint(0, len(_port_temple_road_pics) - 1, key="procedural:Town/PortStreets.rpy:procedural_randint:205:4")]
        vscene _port_temple_road_pic
        $ scene_runtime.location_text += "\n\nНа дороге к храму Эллоны встречаются беременные женщины: кто-то идет за благословением, кто-то уже почти у самых дверей родильной."
    else:
        call ShowImageSeq("georgett", "port", "port", 3)
    $ scene_runtime.text = scene_runtime.location_text

    if dog.is_stray_here("PortStreets"):
        $ scene_runtime.text += "\n\nВ тени стены крутится бродячий пес, настороженно поглядывающий на прохожих."
        $ scene_runtime.location_text = scene_runtime.text

    python:
        main_ui_runtime.action_items = rooms.current.build_action_items()
        main_ui_runtime.action_items.extend(rooms.current.build_exit_items())
    $ rooms.get("PortStreets").mark_visited()
    while True:
        call screen main_ui

label PortStreetsBottleMenu(object_id="port_empty_bottle"):
    $ renpy.dynamic("_port_bottle", "_room_object", "_port_bottle_action")
    $ _port_bottle = None
    python:
        for _room_object in rooms.current.visible_objects():
            if getattr(_room_object, "object_id", "") == "port_empty_bottle":
                _port_bottle = _room_object
                break
    if _port_bottle is None:
        $ main_ui_runtime.action_title = "Действия"
        $ main_ui_runtime.action_items = rooms.current.build_action_items() + rooms.current.build_exit_items()
        return
    $ main_ui_runtime.action_title = _port_bottle.name
    $ scene_runtime.text = _port_bottle.description
    $ scene_runtime.location_text = scene_runtime.text
    python:
        main_ui_runtime.action_items = []
        for _port_bottle_action in _port_bottle.visible_actions():
            if str(_port_bottle_action.hook or "") == "call" and str(_port_bottle_action.target or ""):
                main_ui_runtime.action_items.append(MenuItem(_port_bottle_action.label, Call(_port_bottle_action.target)))
        main_ui_runtime.action_items.append(MenuItem("Назад", Jump("PortStreets")))
    return


label PortStreetsExamineLanes:
    $ renpy.dynamic("_port_lanes_pictures", "_port_lanes_picture")
    $ _port_lanes_pictures = ["images/general/port_streets.png", "images/general/port_streets1.png", "images/general/port_streets2.png", "images/general/port_streets4.png", "images/general/port_streets5.png"]
    $ _port_lanes_picture = _port_lanes_pictures[procedural_randint(0, len(_port_lanes_pictures) - 1, key="procedural:Town/PortStreets.rpy:procedural_randint:292:5")]
    $ scene_runtime.picture = _port_lanes_picture
    vscene _port_lanes_picture
    $ scene_runtime.text = "В этих темных углах любой искатель приключений может найти острые ощущения, которые удовлетворят его вкусы, а при неудаче, возможно, и его смерть."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_items = rooms.current.build_action_items() + rooms.current.build_exit_items()
    return


label PortStreetsExamineEmptyBottle:
    $ scene_runtime.text = "Обычная пустая стеклянная бутылка. Если ее отмыть, она еще вполне пригодится в хозяйстве."
    $ scene_runtime.location_text = scene_runtime.text
    call PortStreetsBottleMenu("port_empty_bottle")
    return


label PortStreetsTakeEmptyBottle:
    if not port_streets_empty_bottle_visible():
        $ main_ui_runtime.action_items = rooms.current.build_action_items() + rooms.current.build_exit_items()
        return
    $ rooms.get("PortStreets").custom_properties["bottle_present"] = 0
    $ player.add_item("empty_bottle_001", 1)
    $ scene_runtime.text = "Вы подбираете пустую бутылку. Стекло цело, и если ее как следует отмыть, она еще пригодится."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_items = rooms.current.build_action_items() + rooms.current.build_exit_items()
    return
