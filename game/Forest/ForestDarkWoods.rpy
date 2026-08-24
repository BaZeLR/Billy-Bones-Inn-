# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    ForestDarkWoodsRoomDefinition = Room(
        code_name="ForestDarkWoods",
        group_name=ROOM_GROUP_FOREST,
        display_name="Темный лес",
        bg_picture="images/forest/darkForest.png",
        descriptions=[
            RoomDescription(
                text="Под сводом густых крон здесь заметно темнее, чем в остальных местах. Между стволами лежат глубокие тени, а под ногами хрустит сухой валежник.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в лес", target="Forest"),
            RoomExit(label="Подойти к пещере", target="ForestCave"),
            RoomExit(label="Вернуться к трактиру", target="StreetTavern"),
        ],
        game_items=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="06:00", end="19:29", condition=forest_open_hours_visible),
        custom_properties={
            "spawn_rules": [
                {"item_id": "mushroom_001", "frequency": 2, "units": 3},
                {"item_id": "honey_comb_001", "frequency": 5, "units": 1},
                {"item_id": "lumber_001", "frequency": 3, "units": 1},
            ],
        },
    )


label ForestDarkWoods:
    $ renpy.dynamic("_forest_spawned")
    $ rooms.enter("ForestDarkWoods")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ scene_runtime.text = rooms.get("ForestDarkWoods").descriptions[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ _forest_spawned = forest_room_spawn(rooms.get("ForestDarkWoods"))
    if len(_forest_spawned) > 0:
        $ scene_runtime.text = scene_runtime.text + "\n\nВ тенях между стволами можно наткнуться на кое-что полезное."
        $ scene_runtime.location_text = scene_runtime.text
        $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ main_ui_runtime.action_title = "Темный лес"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.action_items = forest_subroom_action_items(rooms.current)
    while True:
        call screen main_ui
