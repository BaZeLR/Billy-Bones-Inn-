# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def artisans_quarter_exit_minutes(target_room=""):
        if str(target_room or "").strip() == "StreetTavern":
            return navigation_group_travel_minutes()
        return 10

    def artisans_quarter_action_items():
        items = []
        for _artisans_object in rooms.get("ArtisansQuarter").visible_objects():
            items.append(MenuItem(_artisans_object.name, Call("ArtisansQuarterObjectMenu", _artisans_object.object_id)))
        for _artisans_exit in rooms.get("ArtisansQuarter").visible_exits():
            items.append(MenuItem(_artisans_exit.label, movement_actions(_artisans_exit.target, artisans_quarter_exit_minutes(_artisans_exit.target))))
        return items

    ArtisansQuarterRoomDefinition = Room(
        code_name="ArtisansQuarter",
        display_name="Квартал ремесленников",
        bg_picture="bg ArtisansQuarter",
        descriptions=[
            RoomDescription(
                text="Вы находитесь в квартале ремесленников, на улице Плотников. Тщательно замощенные камнем мостовые, нарядно раскрашенные вывески, ладно построенные дома выдают богатство этого квартала. Здесь располагаются разнообразные лавки и мастерские. Для вас непосредственный интерес представляют мастерская столяра Драупнира и лавка модистки, портнихи, швеи и просто мастерицы на все руки Ирмы Фараго. Дальше улица Плотников ведет к богатым кварталам городского нобилитета.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Идти в мастерскую столяра Драупнира", target="StolyarWorkshop", minutes_to_pass=10),
            RoomExit(label="Идти в лавку портнихи Фараго", target="DressShop", minutes_to_pass=10),
            RoomExit(label="Зайти в цирюльню Серджио Пета", target="BarberShop", minutes_to_pass=10),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[
            GameObject(
                object_id="workshops",
                name="Мастерские",
                description="Вдоль улицы тянутся ремесленные лавки и мастерские, каждая со своей вывеской и запахом работы.",
                actions=[
                    ObjectAction(
                        action_id="examine_workshops",
                        label="Осмотреть мастерские",
                        hook="text",
                        target="На этой улице трудятся хорошие мастера. Тут можно найти и столяра Драупнира, и лавку Ирмы Фараго, и цирюльню болтливого Серджио Пета.",
                    ),
                ],
            ),
            GameObject(
                object_id="farago_shop_sign",
                name="Вывеска Фараго",
                description="Яркая вывеска лавки Ирмы сразу бросается в глаза.",
                actions=[
                    ObjectAction(
                        action_id="examine_farago_sign",
                        label="Осмотреть вывеску",
                        hook="text",
                        target="Вывеска обещает, что здесь сошьют все: от простого платья до наряда для важного господина.",
                    ),
                ],
            ),
        ],
        state={
            "display_text": "",
        },
    )


label ArtisansQuarter:
    $ renpy.dynamic("_artisans_desc_rows")
    $ rooms.enter("ArtisansQuarter")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.object_id = ""
    $ dress_shop.girl_dress_block = 0
    $ _artisans_desc_rows = rooms.current.visible_descriptions()
    if len(_artisans_desc_rows) > 0:
        $ scene_runtime.text = _artisans_desc_rows[0].text
    else:
        $ scene_runtime.text = "Вы находитесь в квартале ремесленников."
    $ scene_runtime.text += "\n\nМежду портновской лавкой и мастерской столяра примостилась цирюльня Серджио Пета: оттуда тянет мылом, горячими полотенцами и нескончаемыми городскими сплетнями."
    if dog.is_stray_here("ArtisansQuarter"):
        $ scene_runtime.text += "\n\nУ края мостовой крутится бродячий пес, заглядывающий в мастерские в поисках чего-нибудь съестного."
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.get("ArtisansQuarter").state["display_text"] = scene_runtime.text
    $ rooms.current.mark_visited()

    call ShowImageSeq("general", "", "LocArtisansQuarter", 4)

    call RoomEnterEventGate(rooms.current_code, False)

    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = artisans_quarter_action_items()
    while True:
        call screen main_ui


label ArtisansQuarterObjectMenu(object_id=""):
    $ renpy.dynamic("_artisans_object", "_room_object", "_artisans_action", "_artisans_args")
    $ _artisans_object = None
    python:
        for _room_object in rooms.get("ArtisansQuarter").visible_objects():
            if getattr(_room_object, "object_id", "") == str(object_id or ""):
                _artisans_object = _room_object
                break

    if _artisans_object is None:
        $ main_ui_runtime.action_items = artisans_quarter_action_items()
        return

    $ scene_runtime.text = _artisans_object.description
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = _artisans_object.name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []

    python:
        for _artisans_action in _artisans_object.visible_actions():
            _artisans_args = tuple(getattr(_artisans_action, "args", ()) or ())
            if _artisans_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_artisans_action.label, Call("ArtisansQuarterObjectText", object_id, _artisans_action.action_id)))
            elif _artisans_action.hook == "call" and str(_artisans_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_artisans_action.label, Call(_artisans_action.target, *_artisans_args)))
            elif _artisans_action.hook == "jump" and str(_artisans_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_artisans_action.label, Jump(_artisans_action.target)))

    $ main_ui_runtime.action_items.append(MenuItem("Назад", [
        SetField(scene_runtime, "text", str(rooms.get("ArtisansQuarter").state.get("display_text", "") or "")),
        SetField(scene_runtime, "location_text", str(rooms.get("ArtisansQuarter").state.get("display_text", "") or "")),
        SetField(main_ui_runtime, "action_title", "Действия"),
        SetField(main_ui_runtime, "action_content", None),
        SetField(main_ui_runtime, "action_items", artisans_quarter_action_items()),
        Function(main_ui_restart_interaction),
    ]))
    return


label ArtisansQuarterObjectText(object_id="", action_id=""):
    $ renpy.dynamic("_artisans_name", "_artisans_text", "_room_action", "_room_object")
    python:
        _artisans_text = ""
        _artisans_name = ""
        for _room_object in rooms.get("ArtisansQuarter").visible_objects():
            if getattr(_room_object, "object_id", "") != str(object_id or ""):
                continue
            _artisans_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _artisans_text = str(_room_action.target or "")
                    break
            break
        if _artisans_text:
            scene_runtime.text = _artisans_text
            scene_runtime.location_text = _artisans_text
            main_ui_runtime.action_title = _artisans_name or "Действия"
    call ArtisansQuarterObjectMenu(object_id)
    return
