init 6 python:
    ForestCaveRoom = Room(
        code_name="ForestCave",
        display_name="Пещера",
        bg_picture="",
        descriptions=[
            RoomDescription(
                text="В глубине темного леса темнеет невысокий вход в пещеру. Внутри тянет сыростью и прохладой, а дальше все скрывает полумрак.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться к темному лесу", target="ForestDarkWoods"),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[],
        npcs=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "spawn_rules": [
                {"item_id": "mushroom_001", "frequency": 2, "units": 2},
                {"item_id": "moss_001", "frequency": 2, "units": 2},
            ],
        },
    )


label ForestCave:
    call EnterLocation("ForestCave")
    $ CurrentRoom = ForestCaveRoom
    $ CurLoc = "ForestCave"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = ForestCaveRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    $ _forest_spawned = forest_room_spawn(ForestCaveRoom)
    if len(_forest_spawned) > 0:
        $ MainTxt = MainTxt + "\n\nДаже здесь можно отыскать кое-что съедобное или полезное."
        $ CurLocDesc = MainTxt
        $ ForestSubroomSavedText = MainTxt
    $ current_action_title = "Пещера"
    $ current_action_content = None
    $ current_action_items = []
    call ForestSubroomBuildActions
    jump ForestCaveView


label ForestCaveView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump ForestCaveView
