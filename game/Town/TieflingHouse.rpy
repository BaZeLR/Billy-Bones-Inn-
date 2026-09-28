init python:
    TieflingHouseRoomDefinition = Room(
        code_name="TieflingHouse",
        group_name=ROOM_GROUP_CITY,
        display_name="Зелёный дом",
        bg_picture="images/nostar/nobility_quarters.png",
        descriptions=[RoomDescription(
            text="У зелёного дома утихли голоса соседок. В окне дрожит свеча; за тяжёлой дверью слышен звон стекла и нетерпеливые шаги. На косяке остались свежие царапины, словно хозяйка захлопывала дверь перед гостями не раз.",
            priority=100,
        )],
        exits=[RoomExit(label="Вернуться в квартал знати", target="NobilityQuarters", minutes_to_pass=5)],
        schedule=RoomSchedule(
            start="09:00",
            end="20:59",
            closed_text="Окна зелёного дома темны, дверь заперта. Придётся вернуться в часы приёма.",
        ),
    )


label TieflingHouse:
    $ rooms.enter("TieflingHouse")
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""
    $ main_ui_runtime.action_title = rooms.current.display_name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    vscene rooms.current.bg_picture
    if rooms.current.is_open():
        $ scene_runtime.text = rooms.current.visible_descriptions()[0].text
    else:
        $ scene_runtime.text = rooms.current.schedule.closed_text
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.current.mark_visited()
    if rooms.current.is_open():
        call RoomEnterEventGate(rooms.current_code, False)
    $ main_ui_runtime.action_items = rooms.current.build_exit_items()
    while True:
        call screen main_ui
