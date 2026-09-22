init 6 python:
    ShedWashroomDefinition = Room(
        code_name="ShedWashroom",
        display_name="Прачечная и купальня",
        group_name=ROOM_GROUP_TAVERN,
        is_hidden=True,
        bg_picture="images/tavern/backyard/shed/washroom.png",
        descriptions=[RoomDescription(
            text="Это отдельная комната в отремонтированном сарае. Здесь стоят купель, корыто для стирки и скамья; на полках сложены полотенца и белье. Плотная дверь отделяет прачечную от соседнего помещения с печью и запасом дров.",
            priority=100,
        )],
        exits=[RoomExit(label="Вернуться к печи и поленнице", target="Shed", minutes_to_pass=1)],
        game_items=["shed_wash_tub"],
        custom_properties={"object_menu_label": "ShedWashroomBath"},
    )

    def shed_washroom_picture():
        if 6 <= int(calendar_v2.hour) < 20:
            return "images/tavern/backyard/shed/washroom.png"
        return "images/tavern/backyard/shed/washroom_night.png"

label ShedWashroom:
    if rooms.get("ShedWashroom").is_hidden or not tavern.renovation_complete("shed"):
        jump Shed
    $ rooms.enter("ShedWashroom")
    call RoomEnterEventGate(rooms.current_code, False)
    $ scene_runtime.picture = shed_washroom_picture()
    $ scene_runtime.text = rooms.current.visible_descriptions()[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.current.mark_visited()
    $ main_ui_runtime.action_title = "Прачечная и купальня"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    while True:
        call screen main_ui
