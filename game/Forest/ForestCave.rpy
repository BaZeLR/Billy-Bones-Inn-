# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def forest_cave_picture():
        if forest_after_dusk() and renpy.loadable("images/forest/cave_night.png"):
            return "images/forest/cave_night.png"
        if renpy.loadable("images/forest/cave_day.png"):
            return "images/forest/cave_day.png"
        return ""

    ForestCaveRoomDefinition = Room(
        code_name="ForestCave",
        group_name=ROOM_GROUP_FOREST,
        display_name="Пещера",
        bg_picture="images/forest/cave_day.png",
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
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="06:00", end="19:29", condition=forest_open_hours_visible),
        custom_properties={
            "spawn_rules": [
                {"item_id": "mushroom_001", "frequency": 2, "units": 2},
                {"item_id": "moss_001", "frequency": 2, "units": 2},
            ],
        },
    )


label ForestCave:
    $ renpy.dynamic("_forest_spawned")
    $ rooms.enter("ForestCave")
    $ scene_runtime.picture = forest_cave_picture() or rooms.current.bg_picture or None
    $ scene_runtime.text = rooms.get("ForestCave").descriptions[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ _forest_spawned = forest_room_spawn(rooms.get("ForestCave"))
    if len(_forest_spawned) > 0:
        $ scene_runtime.text = scene_runtime.text + "\n\nДаже здесь можно отыскать кое-что съедобное или полезное."
        $ scene_runtime.location_text = scene_runtime.text
        $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ main_ui_runtime.action_title = "Пещера"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.action_items = forest_subroom_action_items(rooms.current)
    while True:
        call screen main_ui
