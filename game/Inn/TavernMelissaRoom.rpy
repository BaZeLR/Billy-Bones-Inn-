# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_melissa_room_sleep_picture():
        picture_cycle = MelissaStaticData.image_sequence("tavern", "sleep")
        if len(picture_cycle) > 0:
            return picture_cycle[int(current_game_day() or 0) % len(picture_cycle)]
        return ""

    def tavern_melissa_room_can_show_sleeping():
        temp_room = str(Melissa.temp_room_code or "").strip()
        if temp_room and threads["melissaBatProblem"].num < 10:
            return False
        if str(people.location("melissa") or "") != "TavernMelissaRoom":
            return False
        return (not people.is_awake("melissa")) or (household_morning_issue_type("melissa") == "sleepy" and int(calendar_v2.hour or 0) < 12)

    def tavern_melissa_room_picture():
        if tavern_melissa_room_can_show_sleeping():
            sleep_picture = tavern_melissa_room_sleep_picture()
            if str(sleep_picture or "").strip():
                return sleep_picture
        return "images/tavern/secondfloor/girls_room_day.png"

    def tavern_melissa_room_text():
        text = str(rooms.get("TavernMelissaRoom").descriptions[0].text or "")
        issue_notice = str(household_room_issue_notice_text("melissa") or "").strip()
        if issue_notice:
            text += "\n\n" + issue_notice
        temp_room_notice = str(melissa_temp_room_text() or "").strip()
        if temp_room_notice:
            text += "\n\n" + temp_room_notice
        return werecat_append_visible_text(text, "TavernMelissaRoom")

    def tavern_melissa_room_get_object(object_id):
        object_key = str(object_id or "").strip()
        for room_object in rooms.get("TavernMelissaRoom").visible_game_items():
            if getattr(room_object, "object_id", "") == object_key:
                return room_object
        return None

    def tavern_melissa_room_action_items():
        items = []
        for issue_action in list(household_room_issue_action_specs("melissa") or []):
            items.append(MenuItem(str(issue_action.get("label", "") or ""), Call(str(issue_action.get("target", "") or ""), *tuple(issue_action.get("args", ()) or ()))))
        if tavern_upstairs_can_clean_rooms():
            items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernMelissaRoom", "", "")))
        items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernMelissaRoom")))
        for room_object in rooms.get("TavernMelissaRoom").visible_game_items():
            items.append(MenuItem(room_object.name, Call("TavernMelissaRoomObjectMenu", room_object.object_id)))
        for room_exit in rooms.get("TavernMelissaRoom").visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target)))
        return items

    TavernMelissaRoomRoomDefinition = Room(
        code_name="TavernMelissaRoom",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Комната Мелиссы",
        bg_picture=MelissaStaticData.image_path("tavern", "room") or MelissaStaticData.image_path("portrait", "default"),
        descriptions=[
            RoomDescription(
                text="Вы заглядываете в комнату Мелиссы. Обстановка небогатая: кровать, ларь, табурет и несколько аккуратно сложенных вещей.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в коридор", target="TavernUpstairs"),
        ],
        game_items=[
            bedroom_door_object("melissa_room_door_001", "TavernMelissaRoom", "Мелиссы"),
            "melissa_drawings_booklet_001",
        ],
        custom_properties={
            "object_menu_label": "TavernMelissaRoomObjectMenu",
        },
    )


label TavernMelissaRoom:
    $ rooms.enter("TavernMelissaRoom")
    $ scene_runtime.picture = tavern_melissa_room_picture() or rooms.current.bg_picture or None
    if scene_runtime.picture:
        vscene scene_runtime.picture
    call RoomEnterEventGate(rooms.current_code, False)
    $ scene_runtime.text = tavern_melissa_room_text()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Комната Мелиссы"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
    while True:
        call screen main_ui


label TavernMelissaRoomObjectMenu(object_id="", preserve_text=False):
    $ renpy.dynamic("_room_object")
    $ renpy.dynamic("_melissa_room_has_take_action", "_room_action", "_room_args")
    $ _room_object = tavern_melissa_room_get_object(object_id)
    if _room_object is None:
        $ main_ui_runtime.action_items = tavern_melissa_room_action_items()
        return

    $ main_ui_runtime.object_id = object_id
    if not bool(preserve_text):
        $ scene_runtime.text = bedroom_door_object_text(_room_object)
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(_room_object.name or "Комната Мелиссы")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        _melissa_room_has_take_action = False
        for _room_action in _room_object.visible_actions():
            _room_args = tuple(getattr(_room_action, "args", ()) or ())
            if str(getattr(_room_action, "target", "") or "") == "Take":
                _melissa_room_has_take_action = True
            if _room_action.hook == "call" and str(_room_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif _room_action.hook == "jump" and str(_room_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        if bool(getattr(_room_object, "carriable", False)) and not _melissa_room_has_take_action:
            main_ui_runtime.action_items.append(MenuItem("Взять", Call("Take", object_id, "TavernMelissaRoom", "", object_id)))
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "picture", tavern_melissa_room_picture() or rooms.get("TavernMelissaRoom").bg_picture or None),
            SetField(scene_runtime, "text", tavern_melissa_room_text()),
            SetField(scene_runtime, "location_text", tavern_melissa_room_text()),
            SetField(main_ui_runtime, "action_title", "Комната Мелиссы"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", tavern_melissa_room_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


