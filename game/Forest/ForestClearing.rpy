# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    ForestClearingRoomDefinition = Room(
        code_name="ForestClearing",
        group_name=ROOM_GROUP_FOREST,
        display_name="Малая поляна",
        bg_picture="images/forest/small_clearing.png",
        descriptions=[
            RoomDescription(
                text="Небольшая лесная поляна освещена солнцем. Здесь чуть суше, чем под деревьями, а трава примята следами зверей и людей.",
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
                {"item_id": "berries_001", "frequency": 2, "units": 3},
                {"item_id": "honey_comb_001", "frequency": 4, "units": 1},
                {"item_id": "lavender_001", "frequency": 3, "units": 1},
                {"item_id": "wild_rose_001", "frequency": 3, "units": 1},
                {"item_id": "special_herbs_001", "frequency": 4, "units": 1},
            ],
        },
    )


label ForestClearing:
    $ renpy.dynamic("_clara_forest_picture", "_forest_spawned")
    $ rooms.enter("ForestClearing")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    $ scene_runtime.text = rooms.get("ForestClearing").descriptions[0].text
    if str(people.location("clara") or "") == "ForestClearing":
        $ _clara_forest_picture = Clara.forest_picture("ForestClearing")
        if str(_clara_forest_picture or "").strip():
            $ scene_runtime.picture = _clara_forest_picture
        $ scene_runtime.text = scene_runtime.text + "\n\nНа краю поляны вы замечаете Клариссу, явно вышедшую сюда прогуляться и подышать лесным воздухом."
    $ scene_runtime.location_text = scene_runtime.text
    $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ _forest_spawned = forest_room_spawn(rooms.get("ForestClearing"))
    if len(_forest_spawned) > 0:
        $ scene_runtime.text = scene_runtime.text + "\n\nНа поляне можно кое-что найти, если осмотреть траву и кусты."
        $ scene_runtime.location_text = scene_runtime.text
        $ forest_room_set_saved_text(scene_runtime.text, rooms.current)
    $ main_ui_runtime.action_title = "Поляна"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.action_items = forest_subroom_action_items(rooms.current)
    while True:
        call screen main_ui
