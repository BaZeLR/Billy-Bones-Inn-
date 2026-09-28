init 6 python:
    ShedRuinedChamberDefinition = Room(
        code_name="ShedRuinedChamber",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Каморка со старой печью",
        bg_picture="images/tavern/backyard/shed/ruined_stove_chamber.png",
        descriptions=[
            RoomDescription(
                text="За покосившейся перегородкой вы находите тесную каморку. Пол здесь холодный, в углах осыпалась штукатурка, а большую часть дальней стены занимает старая, наполовину развалившаяся печь.",
                first_time=True,
                priority=200,
            ),
            RoomDescription(
                text="В скрытой каморке за перегородкой стоит старая развалившаяся печь. Сюда почти не заглядывают во время обычных хозяйственных дел.",
                priority=100,
            ),
        ],
        exits=[RoomExit(label="Вернуться в сарай", target="Shed", minutes_to_pass=1)],
        game_items=["shed_ruined_stove"],
        is_hidden=True,
    )


label ShedRuinedChamber:
    if rooms.get("ShedRuinedChamber").is_hidden or tavern.renovation_complete("shed"):
        jump Shed
    $ rooms.enter("ShedRuinedChamber")
    call RoomEnterEventGate(rooms.current_code, False)
    if 6 <= int(calendar_v2.hour or 0) < 20:
        $ scene_runtime.picture = "images/tavern/backyard/shed/ruined_stove_chamber.png"
    else:
        $ scene_runtime.picture = "images/tavern/backyard/shed/ruined_stove_chamber_night.png"
    $ scene_runtime.text = rooms.current.visible_descriptions()[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.current.mark_visited()
    $ main_ui_runtime.action_title = rooms.current.display_name
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = rooms.current.build_exit_items() + rooms.current.build_action_items()
    while True:
        call screen main_ui
