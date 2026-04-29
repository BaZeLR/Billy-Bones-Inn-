# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_upstairs_can_enter_amanda_room():
        return int(AmandaVar.get("kickyoufromroom", 0) or 0) == 0

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
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={},
    )


label TavernUpstairs:
    call EnterLocation("TavernUpstairs")
    $ CurrentRoom = TavernUpstairsRoom
    $ CurLoc = "TavernUpstairs"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    call CheckDailyEvent("", "_story_enter", CurLoc, time)
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
    if story_event_available("TavernUpstairs", "enter"):
        $ _upstairs_items.append(MenuItem("Проверить шум из комнаты Мелиссы", Call("checkTriggers", "TavernUpstairs", "enter", 0)))
    if tavern_upstairs_can_clean_rooms():
        $ _upstairs_items.append(MenuItem("Убрать комнаты наверху", Call("DoChore", "clean_upstairs_rooms", "TavernUpstairs", "", "")))
    python:
        for _upstairs_exit in TavernUpstairsRoom.visible_exits():
            _upstairs_items.append(MenuItem(_upstairs_exit.label, Call("AdvanceMovementTime", _upstairs_exit.target)))
    $ main_ui_set_action_panel("Наверху", _upstairs_items, None, "scene", restart=False)
    return


