# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_upstairs_can_enter_amanda_room():
        return not Amanda.room_entry_blocked_today

    def tavern_upstairs_can_clean_rooms():
        try:
            return int(player.chores.weekly.get("clean_upstairs_rooms", 0) or 0) < int(player_chore_target("clean_upstairs_rooms") or 0)
        except Exception:
            return True

    def tavern_upstairs_bedroom_sound_lines():
        lines = []
        for npc_id in ("sandra", "melissa", "amanda"):
            room_code = "Tavern%sRoom" % npc_id.capitalize()
            info = people.get_info(npc_id)
            if str(people.location(npc_id) or "") != room_code or info is None or int(info.arousal_value() or 0) < 65:
                continue
            lines.append("За дверью комнаты, где сейчас находится {}, слышится размеренный скрип кровати. Похоже, сегодня ей слишком трудно лежать спокойно.".format(_action_display_name(npc_id)))
        return lines

    def tavern_upstairs_description():
        lines = [rooms.get("TavernUpstairs").descriptions[0].text]
        lines.extend(tavern_upstairs_bedroom_sound_lines())
        return "\n\n".join([str(row or "").strip() for row in lines if str(row or "").strip()])

    def tavern_upstairs_action_items():
        items = []
        if tavern_upstairs_can_clean_rooms():
            items.append(MenuItem("Убрать комнаты наверху", Call("DoChore", "clean_upstairs_rooms", "TavernUpstairs", "", "")))
        for room_exit in rooms.get("TavernUpstairs").visible_exits():
            target = str(room_exit.target or "")
            if target in ("TavernMain", "TavernStorage") and not player_can_leave_second_floor():
                continue
            if target == "TavernAmandaRoom":
                items.append(MenuItem(room_exit.label, Call("TavernAmandaRoomDoor")))
            else:
                items.append(MenuItem(room_exit.label, movement_actions(target)))
        if not player_can_leave_second_floor():
            items.append(MenuItem(player_public_movement_block_text(), movement_actions("TavernMyRoom")))
        return items

    TavernUpstairsRoomDefinition = Room(
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
    $ rooms.enter("TavernUpstairs")
    $ scene_runtime.picture = rooms.current.bg_picture or None
    call RoomEnterEventGate(rooms.current_code, False)
    $ scene_runtime.text = tavern_upstairs_description()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Наверху"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_upstairs_action_items()
    $ main_ui_runtime.mode = "scene"
    while True:
        call screen main_ui


