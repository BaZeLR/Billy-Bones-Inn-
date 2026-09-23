# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_empty_room_picture():
        if tavern.renovation_complete("guest_room"):
            return "images/amanda/Room/emptyroom.jpg"
        return rooms.get("TavernEmptyRoom").bg_picture

    def tavern_empty_room_description():
        if tavern.renovation_complete("guest_room"):
            return "Гостевая комната отремонтирована: добротная кровать с занавесями, шкаф и стол превращают ее в уютную небольшую гостиную. Здесь удобно принять гостей и спокойно побеседовать."
        text = rooms.get("TavernEmptyRoom").descriptions[0].text
        if tavern.renovation_days_left("guest_room"):
            text += "\n\nДо окончания ремонта осталось дней: %s." % tavern.renovation_days_left("guest_room")
        return text

    def tavern_empty_room_peephole_visible():
        return int(player.tavern_management.client_room_hole or 0) > 0

    def tavern_empty_room_peephole_has_client():
        if not player.tavern_management.isTavernOpen or int(player.tavern_management.client_room_hole or 0) <= 0:
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
        description="В стене вашей комнаты спрятано потайное окошко, за которое вы заплатили Драупниру. Отсюда можно наблюдать за происходящим в гостевой.",
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
        if tavern_upstairs_can_clean_rooms():
            items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernEmptyRoom", "", "")))
        items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernEmptyRoom")))
        for room_exit in rooms.get("TavernEmptyRoom").visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target)))
        return items

    TavernEmptyRoomRoomDefinition = Room(
        code_name="TavernEmptyRoom",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Гостевая комната",
        bg_picture="bg amanda_room",
        descriptions=[
            RoomDescription(
                text="Вы открываете гостевую комнату. Здесь пока почти ничего нет: голая кровать, голые стены и пыль в углах. Сейчас комната никем не занята.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в коридор", target="TavernUpstairs"),
        ],
        game_items=[],
        custom_properties={},
    )


label TavernEmptyRoom:
    $ rooms.enter("TavernEmptyRoom")
    call RoomEnterEventGate(rooms.current_code, False)
    $ scene_runtime.picture = tavern_empty_room_picture()
    $ scene_runtime.text = tavern_empty_room_description()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = rooms.get("TavernEmptyRoom").display_name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_empty_room_action_items()
    while True:
        call screen main_ui




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
    $ main_ui_begin_native_scene_state("Потайное окошко")
    show screen main_ui
    vscene "images/amanda/Room/emptyroom.jpg"
    "Вы осторожно проверяете потайное окошко из своей комнаты, но в гостевой сейчас никого нет. Остается только вернуться позже."
    menu:
        "Закрыть окошко":
            pass
    $ main_ui_end_native_scene_state()
    return
