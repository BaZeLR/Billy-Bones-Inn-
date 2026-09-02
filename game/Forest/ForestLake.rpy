# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    ForestLakeRoomDefinition = Room(
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
    $ renpy.dynamic("_forest_spawned")
    $ rooms.enter("ForestLake")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ scene_runtime.text = rooms.get("ForestLake").descriptions[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ _forest_spawned = forest_room_spawn(rooms.get("ForestLake"))
    if len(_forest_spawned) > 0:
        $ scene_runtime.text = scene_runtime.text + "\n\nПо берегу озера можно найти кое-что полезное."
        $ scene_runtime.location_text = scene_runtime.text
        $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ main_ui_runtime.action_title = "Озеро"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.action_items = forest_subroom_action_items(rooms.current)
    while True:
        call screen main_ui
