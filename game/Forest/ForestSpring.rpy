# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    ForestSpringRoom = Room(
        code_name="ForestSpring",
        group_name=ROOM_GROUP_FOREST,
        display_name="Родник",
        bg_picture="images/forest/seclude_lake_1.png",
        descriptions=[
            RoomDescription(
                text="В стороне от основной тропы из земли бьет холодный лесной родник. Вода чистая и прозрачная, вокруг влажный мох и корни деревьев.",
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
                {"item_id": "mushroom_001", "frequency": 2, "units": 2},
                {"item_id": "berries_001", "frequency": 2, "units": 2},
                {"item_id": "lavender_001", "frequency": 3, "units": 1},
                {"item_id": "special_herbs_001", "frequency": 4, "units": 1},
            ],
        },
    )


label ForestSpring:
    $ CurrentRoom = ForestSpringRoom
    $ CurLoc = "ForestSpring"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = ForestSpringRoom.descriptions[0].text
    if str(getLocation("clara") or "") == "ForestSpring":
        $ _clara_forest_picture = clara_forest_picture("ForestSpring")
        if str(_clara_forest_picture or "").strip():
            $ _layout_last_picture = _clara_forest_picture
        $ MainTxt = MainTxt + "\n\nУ родника вы замечаете Клариссу, которая явно наслаждается прохладой и тишиной этого места."
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    $ _forest_spawned = forest_room_spawn(ForestSpringRoom)
    if len(_forest_spawned) > 0:
        $ MainTxt = MainTxt + "\n\nУ воды и под кустами можно кое-что найти."
        $ CurLocDesc = MainTxt
        $ ForestSubroomSavedText = MainTxt
    $ current_action_title = "Родник"
    $ current_action_content = None
    $ current_action_items = []
    call ForestSubroomBuildActions
    $ _forest_spring_ui_return = None
    while _forest_spring_ui_return is None:
        call screen main_ui
        $ _forest_spring_ui_return = _return
    jump ForestSpring


