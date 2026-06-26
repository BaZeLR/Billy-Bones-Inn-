# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    ForestLakeRoom = Room(
        code_name="ForestLake",
        group_name=ROOM_GROUP_FOREST,
        display_name="Уединенное озеро",
        bg_picture="images/forest/seclude_lake.png",
        descriptions=[
            RoomDescription(
                text="Среди деревьев открылось небольшое озеро. Вода спокойная, берега заросли травой, а вокруг стоит приятная лесная тишина.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться на скрытую тропу", target="ForestHiddenPath"),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="06:00", end="19:29", condition=forest_open_hours_visible),
        custom_properties={
            "spawn_rules": [
                {"item_id": "mushroom_001", "frequency": 2, "units": 2},
                {"item_id": "berries_001", "frequency": 3, "units": 2},
                {"item_id": "wild_rose_001", "frequency": 3, "units": 1},
            ],
        },
    )


label ForestLake:
    $ CurrentRoom = ForestLakeRoom
    $ CurLoc = "ForestLake"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = ForestLakeRoom.descriptions[0].text
    if str(getLocation("clara") or "") == "ForestLake":
        $ _clara_forest_picture = clara_forest_picture("ForestLake")
        if str(_clara_forest_picture or "").strip():
            $ _layout_last_picture = _clara_forest_picture
        $ MainTxt = MainTxt + "\n\nУ воды вы замечаете Клариссу, которая, похоже, решила ненадолго скрыться от городской суеты."
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    $ _forest_spawned = forest_room_spawn(ForestLakeRoom)
    if len(_forest_spawned) > 0:
        $ MainTxt = MainTxt + "\n\nПо берегу озера можно найти кое-что полезное."
        $ CurLocDesc = MainTxt
        $ ForestSubroomSavedText = MainTxt
    $ current_action_title = "Озеро"
    $ current_action_content = None
    $ current_action_items = []
    call ForestSubroomBuildActions
    $ _forest_lake_ui_return = None
    while _forest_lake_ui_return is None:
        call screen main_ui
        $ _forest_lake_ui_return = _return
    jump ForestLake


