init 6 python:
    ForestClearingRoom = Room(
        code_name="ForestClearing",
        group_name=ROOM_GROUP_FOREST,
        display_name="Малая поляна",
        bg_picture="",
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
        npcs=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
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
    call EnterLocation("ForestClearing")
    $ CurrentRoom = ForestClearingRoom
    $ CurLoc = "ForestClearing"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = ForestClearingRoom.descriptions[0].text
    if str(getLocation("clara") or "") == "ForestClearing":
        $ _clara_forest_picture = clara_forest_picture("ForestClearing")
        if str(_clara_forest_picture or "").strip():
            $ _layout_last_picture = _clara_forest_picture
        $ MainTxt = MainTxt + "\n\nНа краю поляны вы замечаете Клариссу, явно вышедшую сюда прогуляться и подышать лесным воздухом."
    $ CurLocDesc = MainTxt
    $ ForestSubroomSavedText = MainTxt
    $ _forest_spawned = forest_room_spawn(ForestClearingRoom)
    if len(_forest_spawned) > 0:
        $ MainTxt = MainTxt + "\n\nНа поляне можно кое-что найти, если осмотреть траву и кусты."
        $ CurLocDesc = MainTxt
        $ ForestSubroomSavedText = MainTxt
    $ current_action_title = "Поляна"
    $ current_action_content = None
    $ current_action_items = []
    call ForestSubroomBuildActions
    jump ForestClearingView


label ForestClearingView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump ForestClearingView
