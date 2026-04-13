init 6 python:
    ForestHiddenPathRoom = Room(
        code_name="ForestHiddenPath",
        display_name="Скрытая тропа",
        bg_picture="images/forest/hidden_path.png",
        descriptions=[
            RoomDescription(
                text="Едва заметная тропка уходит между кустами и деревьями в сторону от обычных путей. Здесь тихо, и кажется, что сюда редко кто заходит.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в лес", target="Forest"),
            RoomExit(label="Пройти к уединенному озеру", target="ForestLake"),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[],
        npcs=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "spawn_rules": [
                {"item_id": "berries_001", "frequency": 2, "units": 2},
                {"item_id": "honey_comb_001", "frequency": 4, "units": 1},
            ],
        },
    )


label ForestHiddenPath:
    call EnterLocation("ForestHiddenPath")
    $ CurrentRoom = ForestHiddenPathRoom
    $ CurLoc = "ForestHiddenPath"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = ForestHiddenPathRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    $ _forest_spawned = forest_room_spawn(ForestHiddenPathRoom)
    if len(_forest_spawned) > 0:
        $ MainTxt = MainTxt + "\n\nВ зарослях у тропы можно кое-что собрать."
        $ CurLocDesc = MainTxt
        $ ForestSubroomSavedText = MainTxt
    $ current_action_title = "Скрытая тропа"
    $ current_action_content = None
    $ current_action_items = []
    call ForestSubroomBuildActions
    jump ForestHiddenPathView


label ForestHiddenPathView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump ForestHiddenPathView
