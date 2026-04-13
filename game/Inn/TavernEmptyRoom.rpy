init 6 python:
    TavernEmptyRoomRoom = Room(
        code_name="TavernEmptyRoom",
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
        game_items=[],
        npcs=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={},
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
    jump TavernEmptyRoomView


label TavernEmptyRoomBuildActions:
    $ current_action_title = "Пустая комната"
    $ current_action_content = None
    $ current_action_items = []
    if tavern_upstairs_can_clean_rooms():
        $ current_action_items.append(MenuItem("Прибрать комнату", Call("DoChore", "clean_upstairs_rooms", "TavernEmptyRoom", "", "")))
    $ current_action_items.append(MenuItem("Осмотреть комнату получше", Call("UpstairsRoomSearch", "TavernEmptyRoom", "TavernEmptyRoomBuildActions")))
    python:
        for _exit in TavernEmptyRoomRoom.visible_exits():
            current_action_items.append(MenuItem(_exit.label, Call("AdvanceMovementTime", _exit.target)))
    return


label TavernEmptyRoomView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernEmptyRoomView
