init python:
    NobilityQuartersRoomDefinition = Room(
        code_name="NobilityQuarters",
        group_name=ROOM_GROUP_CITY,
        display_name="Квартал знати",
        bg_picture="images/nostar/nobility_quarters.png",
        descriptions=[RoomDescription(
            text="За мастерскими мостовая становится шире и чище. Пять больших домов стоят бок о бок: шафрановый, лазурный, багряный, цвета слоновой кости и зелёный. За красивыми дверями здесь берегут не только деньги, но и секреты. У дома леди Ностар Линк вас встречает взглядом невозмутимый привратник.",
            priority=100,
        )],
        exits=[
            RoomExit(label="К дому леди Ностар Линк", target="NostarHouse", minutes_to_pass=5),
            RoomExit(label="Вернуться в квартал ремесленников", target="ArtisansQuarter", minutes_to_pass=10),
        ],
    )


label NobilityQuarters:
    $ rooms.enter("NobilityQuarters")
    $ main_ui_runtime.mode = "scene"
    $ main_ui_runtime.selected_char = ""
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""
    $ main_ui_runtime.action_title = rooms.current.display_name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    vscene rooms.current.bg_picture
    $ scene_runtime.text = rooms.current.visible_descriptions()[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.current.mark_visited()
    call RoomEnterEventGate(rooms.current_code, False)
    $ main_ui_runtime.action_items = rooms.current.build_exit_items()
    while True:
        call screen main_ui
