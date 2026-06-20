# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_empty_room_peephole_visible():
        return int(TavernHole or 0) > 0

    def tavern_empty_room_peephole_has_client():
        return str(TavernClosed or "") == "" and int(TavernHole or 0) > 0 and story_event_available("TavernEmptyRoom", "tavern_client_room")

    def tavern_empty_room_peephole_no_client():
        return int(TavernHole or 0) > 0 and not tavern_empty_room_peephole_has_client()

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
                hook="jump",
                target="TavernEmptyRoomPeekClient",
                condition=tavern_empty_room_peephole_has_client,
            ),
            ObjectAction(
                action_id="peek_empty_client_room",
                label="Проверить окошко",
                hook="jump",
                target="TavernEmptyRoomPeekEmpty",
                condition=tavern_empty_room_peephole_no_client,
            ),
        ],
        custom_properties={},
    )

    TavernEmptyRoomRoom = Room(
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
    call EnterLocation("TavernEmptyRoom")
    $ CurrentRoom = TavernEmptyRoomRoom
    $ CurLoc = "TavernEmptyRoom"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ MainTxt = TavernEmptyRoomRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    call TavernEmptyRoomBuildActions
    $ _empty_room_ui_return = None
    while _empty_room_ui_return is None:
        call screen main_ui
        $ _empty_room_ui_return = _return
    jump TavernEmptyRoom


label TavernEmptyRoomBuildActions:
    $ current_action_title = "Пустая комната"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _empty_room_object in TavernEmptyRoomRoom.visible_objects():
            current_action_items.append(MenuItem(_empty_room_object.name, Call("TavernEmptyRoomObjectMenu", _empty_room_object.object_id)))
    if tavern_upstairs_can_clean_rooms():
        $ current_action_items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernEmptyRoom", "", "")))
    $ current_action_items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernEmptyRoom", "TavernEmptyRoomBuildActions")))
    python:
        for _exit in TavernEmptyRoomRoom.visible_exits():
            current_action_items.append(MenuItem(_exit.label, Call("AdvanceMovementTime", _exit.target)))
    return


label TavernEmptyRoomObjectMenu(object_id=""):
    if str(object_id or "") != "tavern_empty_room_peephole":
        call TavernEmptyRoomBuildActions
        return
    $ current_object_id = object_id
    $ current_action_title = TavernEmptyRoomPeepholeObject.name
    $ current_action_content = None
    $ MainTxt = TavernEmptyRoomPeepholeObject.description
    $ CurLocDesc = MainTxt
    if str(TavernEmptyRoomPeepholeObject.picture or ""):
        $ _layout_last_picture = TavernEmptyRoomPeepholeObject.picture
    $ current_action_items = []
    python:
        for _peephole_action in TavernEmptyRoomPeepholeObject.visible_actions():
            if _peephole_action.hook == "jump" and str(_peephole_action.target or ""):
                current_action_items.append(MenuItem(_peephole_action.label, Jump(_peephole_action.target)))
            elif _peephole_action.hook == "call" and str(_peephole_action.target or ""):
                current_action_items.append(MenuItem(_peephole_action.label, Call(_peephole_action.target, *tuple(getattr(_peephole_action, "args", ()) or ()))))
        current_action_items.append(MenuItem("Назад", Jump("TavernEmptyRoom")))
    return


label TavernEmptyRoomPeekClient:
    if not tavern_empty_room_peephole_has_client():
        jump TavernEmptyRoomPeekEmpty
    call checkTriggers("TavernEmptyRoom", "tavern_client_room", 0)
    jump TavernEmptyRoom


label TavernEmptyRoomPeekEmpty:
    $ _layout_last_picture = "images/amanda/Room/emptyroom.jpg"
    $ MainTxt = "Вы осторожно проверяете потайное окошко, но в комнате сейчас никого нет. Остается только вернуться позже, когда кто-нибудь из посетителей уединится наверху."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Потайное окошко"
    $ current_action_content = None
    $ current_action_items = [MenuItem("Вернуться в комнату", Jump("TavernEmptyRoom"))]
    call screen main_ui
    jump TavernEmptyRoom
