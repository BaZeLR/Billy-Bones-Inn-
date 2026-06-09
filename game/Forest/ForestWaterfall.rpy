# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    ForestWaterfallRoom = Room(
        code_name="ForestWaterfall",
        group_name=ROOM_GROUP_FOREST,
        display_name="Водопад",
        bg_picture="",
        descriptions=[
            RoomDescription(
                text="Над каменным уступом шумит небольшой водопад. В воздухе стоит прохладная водяная пыль, а камни вокруг скользкие от постоянной влаги.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в лес", target="Forest"),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="06:00", end="19:29", condition=forest_open_hours_visible),
        custom_properties={
            "spawn_rules": [
                {"item_id": "mushroom_001", "frequency": 3, "units": 2},
                {"item_id": "lavender_001", "frequency": 4, "units": 1},
                {"item_id": "special_herbs_001", "frequency": 3, "units": 1},
                {"item_id": "moss_001", "frequency": 2, "units": 2},
            ],
        },
    )


label ForestWaterfall:
    call EnterLocation("ForestWaterfall")
    $ CurrentRoom = ForestWaterfallRoom
    $ CurLoc = "ForestWaterfall"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = ForestWaterfallRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    $ _forest_spawned = forest_room_spawn(ForestWaterfallRoom)
    if len(_forest_spawned) > 0:
        $ MainTxt = MainTxt + "\n\nУ сырых камней можно заметить кое-какую лесную добычу."
        $ CurLocDesc = MainTxt
        $ ForestSubroomSavedText = MainTxt
    $ current_action_title = "Водопад"
    $ current_action_content = None
    $ current_action_items = []
    call ForestSubroomBuildActions
    $ _forest_waterfall_ui_return = None
    while _forest_waterfall_ui_return is None:
        call screen main_ui
        $ _forest_waterfall_ui_return = _return
    jump ForestWaterfall


