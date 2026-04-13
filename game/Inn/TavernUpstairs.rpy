init 6 python:
    def tavern_upstairs_can_enter_amanda_room():
        return AmandaVar["kickyoufromroom"] == 0

    def tavern_upstairs_can_clean_rooms():
        try:
            return int(PlayerChoresWeek.get("clean_upstairs_rooms", 0) or 0) < int(player_chore_target("clean_upstairs_rooms") or 0)
        except Exception:
            return True

    TavernUpstairsRoom = Room(
        code_name="TavernUpstairs",
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
            RoomExit(label="Зайти в комнату Сандры", target="TavernSandraRoom", condition=tavern_upstairs_can_enter_sandra_room),
            RoomExit(label="Зайти в комнату Мелиссы", target="TavernMelissaRoom"),
            RoomExit(label="Осмотреть пустую комнату", target="TavernEmptyRoom"),
            RoomExit(label="Спуститься в подвал", target="TavernStorage"),
        ],
        game_items=[],
        npcs=[],
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
    $ MainTxt = TavernUpstairsRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    call TavernUpstairsBuildActions
    jump TavernUpstairsView


label TavernUpstairsBuildActions:
    $ current_action_title = "Наверху"
    $ current_action_content = None
    $ current_action_items = []
    if tavern_upstairs_can_clean_rooms():
        $ current_action_items.append(MenuItem("Убрать комнаты наверху", Call("DoChore", "clean_upstairs_rooms", "TavernUpstairs", "", "")))
    python:
        for _upstairs_exit in TavernUpstairsRoom.visible_exits():
            current_action_items.append(MenuItem(_upstairs_exit.label, Call("AdvanceMovementTime", _upstairs_exit.target)))
    return


label TavernUpstairsView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernUpstairsView
