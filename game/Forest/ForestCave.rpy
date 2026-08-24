# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def forest_cave_picture():
        if int(time or 0) >= 4 and renpy.loadable("images/forest/cave_night.png"):
            return "images/forest/cave_night.png"
        if renpy.loadable("images/forest/cave_day.png"):
            return "images/forest/cave_day.png"
        return ""

    ForestCaveRoom = Room(
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
    $ CurrentRoom = ForestCaveRoom
    $ CurLoc = "ForestCave"
    $ scene_image = forest_cave_picture() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = ForestCaveRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    $ forest_room_set_saved_text(MainTxt, CurrentRoom)
    $ _forest_spawned = forest_room_spawn(ForestCaveRoom)
    if len(_forest_spawned) > 0:
        $ MainTxt = MainTxt + "\n\nДаже здесь можно отыскать кое-что съедобное или полезное."
        $ CurLocDesc = MainTxt
        $ forest_room_set_saved_text(MainTxt, CurrentRoom)
    $ current_action_title = "Пещера"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items = forest_subroom_action_items(CurrentRoom)
    call screen main_ui
    return

