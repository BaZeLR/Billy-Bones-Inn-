# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    ForestWaterfallRoomDefinition = Room(
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
    $ renpy.dynamic("_forest_spawned")
    $ rooms.enter("ForestWaterfall")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ scene_runtime.text = rooms.get("ForestWaterfall").descriptions[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ _forest_spawned = forest_room_spawn(rooms.get("ForestWaterfall"))
    if len(_forest_spawned) > 0:
        $ scene_runtime.text = scene_runtime.text + "\n\nУ сырых камней можно заметить кое-какую лесную добычу."
        $ scene_runtime.location_text = scene_runtime.text
        $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ main_ui_runtime.action_title = "Водопад"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.action_items = forest_subroom_action_items(rooms.current)
    while True:
        call screen main_ui
