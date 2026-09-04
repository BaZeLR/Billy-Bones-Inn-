# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_empty_room_peephole_visible():
        return int(player.tavern_management.client_room_hole or 0) > 0

    def tavern_empty_room_peephole_has_client():
        if tavern_main_closed_text() != "" or int(player.tavern_management.client_room_hole or 0) <= 0:
            return False
        girl_name = str(rooms.get("TavernMain").state.get("client_room_girl", "") or "")
        if girl_name == "georgett":
            return 13 <= int(calendar_v2.hour or 0) <= 15 and Georgett.can_work_tavern() and CheckIfSexEventExist("georgett", 3, "Prostitution") > 0
        return story_event_available("TavernEmptyRoom", "tavern_client_room")

    def tavern_empty_room_peephole_no_client():
        return int(player.tavern_management.client_room_hole or 0) > 0 and not tavern_empty_room_peephole_has_client()

    TavernEmptyRoomPeepholeObject = GameObject(
        object_id="tavern_empty_room_peephole",
        name="Потайное окошко",
        description="В стене аккуратно спрятано потайное окошко, за которое вы заплатили Драупниру. Через него можно проверить, что происходит в комнате.",
        picture="images/amanda/Room/emptyroom.jpg",
        condition=tavern_empty_room_peephole_visible,
        actions=[
            ObjectAction(
                action_id="peek_client_room",
                label="Подглядеть в комнату",
                hook="call",
                target="TavernEmptyRoomPeekClient",
                condition=tavern_empty_room_peephole_has_client,
            ),
            ObjectAction(
                action_id="peek_empty_client_room",
                label="Проверить окошко",
                hook="call",
                target="TavernEmptyRoomPeekEmpty",
                condition=tavern_empty_room_peephole_no_client,
            ),
        ],
        custom_properties={},
    )

    def tavern_empty_room_action_items():
        items = []
        for room_object in rooms.get("TavernEmptyRoom").visible_objects():
            items.append(MenuItem(room_object.name, Call("TavernEmptyRoomObjectMenu", room_object.object_id)))
        if tavern_upstairs_can_clean_rooms():
            items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernEmptyRoom", "", "")))
        items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernEmptyRoom")))
        for room_exit in rooms.get("TavernEmptyRoom").visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target)))
        return items

    TavernEmptyRoomRoomDefinition = Room(
        code_name="TavernEmptyRoom",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Пустая комната",
        bg_picture="bg amanda_room",
        descriptions=[
            RoomDescription(
                text="Вы открываете пустующую комнату. Здесь почти ничего нет: голая кровать, голые стены и пыль в углах. Комната пока никем не занята.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в коридор", target="TavernUpstairs"),
        ],
        game_items=[
            TavernEmptyRoomPeepholeObject,
        ],
        custom_properties={
            "object_menu_label": "TavernEmptyRoomObjectMenu",
        },
    )


label TavernEmptyRoom:
    $ rooms.enter("TavernEmptyRoom")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ scene_runtime.text = rooms.get("TavernEmptyRoom").descriptions[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Пустая комната"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_empty_room_action_items()
    while True:
        call screen main_ui


label TavernEmptyRoomObjectMenu(object_id=""):
    $ renpy.dynamic("_peephole_action")
    if str(object_id or "") != "tavern_empty_room_peephole":
        return
    $ main_ui_runtime.object_id = object_id
    $ main_ui_runtime.action_title = TavernEmptyRoomPeepholeObject.name
    $ main_ui_runtime.action_content = None
    $ scene_runtime.text = TavernEmptyRoomPeepholeObject.description
    $ scene_runtime.location_text = scene_runtime.text
    if str(TavernEmptyRoomPeepholeObject.picture or ""):
        $ scene_runtime.picture = TavernEmptyRoomPeepholeObject.picture
    $ main_ui_runtime.action_items = []
    python:
        for _peephole_action in TavernEmptyRoomPeepholeObject.visible_actions():
            if _peephole_action.hook == "call" and str(_peephole_action.target or ""):
                main_ui_runtime.action_items.append(MenuItem(_peephole_action.label, Call(_peephole_action.target, *tuple(getattr(_peephole_action, "args", ()) or ()))))
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "picture", rooms.get("TavernEmptyRoom").bg_picture or None),
            SetField(scene_runtime, "text", rooms.get("TavernEmptyRoom").descriptions[0].text),
            SetField(scene_runtime, "location_text", rooms.get("TavernEmptyRoom").descriptions[0].text),
            SetField(main_ui_runtime, "action_title", "Пустая комната"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", tavern_empty_room_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    return


label TavernEmptyRoomPeekClient:
    if not tavern_empty_room_peephole_has_client():
        call TavernEmptyRoomPeekEmpty
        return
    if str(rooms.get("TavernMain").state.get("client_room_girl", "") or "") == "georgett":
        call TavernProstClients("georgett")
    else:
        call checkTriggers("TavernEmptyRoom", "tavern_client_room", 0)
    return


label TavernEmptyRoomPeekEmpty:
    $ scene_runtime.picture = "images/amanda/Room/emptyroom.jpg"
    $ scene_runtime.text = "Вы осторожно проверяете потайное окошко, но в комнате сейчас никого нет. Остается только вернуться позже, когда кто-нибудь из посетителей уединится наверху."
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Вернуться в комнату":
            $ scene_runtime.picture = rooms.get("TavernEmptyRoom").bg_picture or None
            $ scene_runtime.text = rooms.get("TavernEmptyRoom").descriptions[0].text
            $ scene_runtime.location_text = scene_runtime.text
            $ main_ui_runtime.action_title = "Пустая комната"
            $ main_ui_runtime.action_items = tavern_empty_room_action_items()
            $ main_ui_restart_interaction()
            return
