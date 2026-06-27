# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_upstairs_can_enter_amanda_room():
        return Amanda.var_int("kickyoufromroom", 0) == 0

    def tavern_upstairs_can_clean_rooms():
        try:
            return int(PlayerChoresWeek.get("clean_upstairs_rooms", 0) or 0) < int(player_chore_target("clean_upstairs_rooms") or 0)
        except Exception:
            return True

    TavernUpstairsRoom = Room(
        code_name="TavernUpstairs",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Коридор наверху",
        bg_picture="images/tavern/secondfloor/second_floor.png",
        descriptions=[
            RoomDescription(
                text="Вы поднимаетесь наверх. Узкий коридор тянется вдоль комнат работников трактира. Половицы поскрипывают под ногами, у стен стоят сундуки и всякая хозяйственная мелочь, а под лестницей темнеет проход в подвальное помещение.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Спуститься в главный зал", target="TavernMain"),
            RoomExit(label="Зайти в вашу комнату", target="TavernMyRoom"),
            RoomExit(label="Заглянуть в комнату Аманды", target="TavernAmandaRoom", condition=tavern_upstairs_can_enter_amanda_room),
            RoomExit(label="Зайти в комнату Сандры", target="TavernSandraRoom"),
            RoomExit(label="Зайти в комнату Мелиссы", target="TavernMelissaRoom"),
            RoomExit(label="Осмотреть пустую комнату", target="TavernEmptyRoom"),
            RoomExit(label="Спуститься в подвал", target="TavernStorage"),
        ],
        game_items=[],
        custom_properties={},
    )


label TavernUpstairs:
    $ CurrentRoom = TavernUpstairsRoom
    $ CurLoc = "TavernUpstairs"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    call RoomEnterEventGate(CurLoc, False)
    $ MainTxt = TavernUpstairsRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    call TavernUpstairsBuildActions
    $ _upstairs_ui_return = None
    while _upstairs_ui_return is None:
        call screen main_ui
        $ _upstairs_ui_return = _return
    jump TavernUpstairs


label TavernUpstairsBuildActions:
    $ _upstairs_items = []
    if tavern_upstairs_can_clean_rooms():
        $ _upstairs_items.append(MenuItem("Убрать комнаты наверху", Call("DoChore", "clean_upstairs_rooms", "TavernUpstairs", "", "")))
    python:
        for _upstairs_exit in TavernUpstairsRoom.visible_exits():
            _target = str(_upstairs_exit.target or "")
            if _target in ("TavernMain", "TavernStorage") and not player_can_leave_second_floor():
                continue
            if _target == "TavernAmandaRoom":
                _upstairs_items.append(MenuItem(_upstairs_exit.label, Call("TavernAmandaRoomDoor")))
            else:
                _upstairs_items.append(MenuItem(_upstairs_exit.label, Call("AdvanceMovementTime", _target)))
        if not player_can_leave_second_floor():
            _upstairs_items.append(MenuItem(player_public_movement_block_text(), Call("AdvanceMovementTime", "TavernMyRoom")))
    $ current_action_title = "Наверху"
    $ current_action_content = None
    $ current_action_items = _upstairs_items
    $ UI_mode = "scene"
    return


