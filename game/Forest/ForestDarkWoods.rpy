# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    ForestDarkWoodsRoom = Room(
        code_name="ForestDarkWoods",
        group_name=ROOM_GROUP_FOREST,
        display_name="Темный лес",
        bg_picture="",
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
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={
            "spawn_rules": [
                {"item_id": "mushroom_001", "frequency": 2, "units": 3},
                {"item_id": "honey_comb_001", "frequency": 5, "units": 1},
                {"item_id": "lumber_001", "frequency": 3, "units": 1},
            ],
        },
    )


label ForestDarkWoods:
    call EnterLocation("ForestDarkWoods")
    $ CurrentRoom = ForestDarkWoodsRoom
    $ CurLoc = "ForestDarkWoods"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = ForestDarkWoodsRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    $ _forest_spawned = forest_room_spawn(ForestDarkWoodsRoom)
    if len(_forest_spawned) > 0:
        $ MainTxt = MainTxt + "\n\nВ тенях между стволами можно наткнуться на кое-что полезное."
        $ CurLocDesc = MainTxt
        $ ForestSubroomSavedText = MainTxt
    $ current_action_title = "Темный лес"
    $ current_action_content = None
    $ current_action_items = []
    call ForestSubroomBuildActions
    $ _forest_dark_woods_ui_return = None
    while _forest_dark_woods_ui_return is None:
        call screen main_ui
        $ _forest_dark_woods_ui_return = _return
    jump ForestDarkWoods


