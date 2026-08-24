# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    ShedRoomDefinition = Room(
        code_name="Shed",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Сарай",
        bg_picture="images/tavern/backyard/shed/shed.png",
        descriptions=[
            RoomDescription(
                text="Вы заходите в сарай. Здесь пахнет сырой древесиной, пылью и старым железом.",
                first_time=True,
                priority=200,
            ),
            RoomDescription(
                text="Небольшой сарай служит складом для дров, инструментов и прочего хозяйственного добра.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться на задний двор", target="Backyard"),
        ],
        game_items=[
            "old_axe_001",
            "lumber_001",
        ],
        custom_properties={},
        state={
            "notice_text": "",
            "notice_pending": False,
            "bucket_found": False,
        },
    )

    def shed_has_lumber(room_obj=None):
        target_room = room_obj if room_obj is not None else rooms.current
        if target_room is None:
            target_room = rooms.get("Shed")
        return _room_has_item_by_id(target_room, "lumber_001")

    def shed_picture():
        current_minutes = (int(calendar_v2.hour or 0) % 24) * 60 + int(calendar_v2.minute or 0)
        if 360 <= current_minutes <= 1170:
            return "images/tavern/backyard/shed/shed.png"
        return "images/tavern/backyard/shed/shed_night.png"

    def build_shed_description(include_notice=True, intro_text=""):
        room_obj = rooms.current if rooms.current is not None else rooms.get("Shed")
        room_item_ids = [get_object_id(row) for row in list(getattr(room_obj, "game_items", []) or [])]
        text_parts = []

        intro_value = str(intro_text or "").strip()
        if intro_value:
            text_parts.append(intro_value)

        if include_notice and bool(rooms.get("Shed").state.get("notice_pending", False)) and str(rooms.get("Shed").state.get("notice_text", "") or "").strip():
            text_parts.append(str(rooms.get("Shed").state.get("notice_text", "") or "").strip())

        chopped_count = _room_item_count_by_id(room_obj, "chopped_wood_001")
        chopped_item = get_game_item("chopped_wood_001", room_obj)
        if chopped_count > 0:
            chopped_name = str(chopped_item.name).strip()
            if chopped_count == 1:
                text_parts.append("В сарае лежат {}. Всего: одна охапка.".format(chopped_name))
            else:
                text_parts.append("В сарае лежат {}. Всего: {} охапок.".format(chopped_name, chopped_count))
        else:
            text_parts.append("Поленница пуста.")

        carried_chopped = int(player.item_count("chopped_wood_001") or 0)
        if carried_chopped > 0:
            text_parts.append("При себе у вас колотые дрова: {}.".format(carried_chopped))

        lumber_count = _room_item_count_by_id(room_obj, "lumber_001")
        lumber_item = get_game_item("lumber_001", room_obj)
        if lumber_count > 0:
            lumber_name = str(lumber_item.name).strip()
            if lumber_count == 1:
                text_parts.append("Здесь лежит {}.".format(lumber_name))
            else:
                text_parts.append("Здесь лежат {}. Всего: {}.".format(lumber_name, lumber_count))
        else:
            text_parts.append("Бревен в сарае не осталось.")

        axe_item = get_game_item("old_axe_001", room_obj)
        axe_name = str(axe_item.name).strip()
        if "old_axe_001" in room_item_ids:
            text_parts.append("На стене висит {}.".format(axe_name))
        elif player.item_count("old_axe_001") > 0 and player_has_equipped_weapon("old_axe_001"):
            text_parts.append("{} заткнут у вас за пояс.".format(axe_name[:1].upper() + axe_name[1:]))
        elif player.item_count("old_axe_001") > 0:
            text_parts.append("{} лежит у вас в сумке.".format(axe_name[:1].upper() + axe_name[1:]))
        else:
            text_parts.append("Крючок для топора пуст.")

        return "\n\n".join([row for row in text_parts if str(row or "").strip()])

    def build_shed_action_items():
        room_obj = rooms.current if rooms.current is not None else rooms.get("Shed")
        items = [MenuItem("Осмотреть сарай", Call("ShedExamine"))]
        seen_object_ids = set()
        hidden_action_ids = {"examine_lumber", "examine_chopped_wood", "take_chopped_wood"}

        for row in list(getattr(room_obj, "game_items", []) or []):
            object_id = get_object_id(row)
            if not object_id or object_id in seen_object_ids:
                continue
            seen_object_ids.add(object_id)
            game_item = get_game_item(object_id, room_obj)
            if game_item is None:
                continue
            for item_action in game_item.visible_actions():
                if str(getattr(item_action, "action_id", "") or "") in hidden_action_ids:
                    continue
                action_args = tuple(getattr(item_action, "args", ()) or ())
                if item_action.hook == "call" and str(item_action.target or "") != "":
                    items.append(MenuItem(item_action.label, Call(item_action.target, *action_args)))
                elif item_action.hook == "jump" and str(item_action.target or "") != "":
                    items.append(MenuItem(item_action.label, Jump(item_action.target)))
                elif item_action.hook == "text":
                    items.append(MenuItem(item_action.label, Call("Examine", object_id, "Shed", item_action.target, object_id)))

        _shed_chopped_count = _room_item_count_by_id(room_obj, "chopped_wood_001")
        if _shed_chopped_count > 0:
            items.append(MenuItem("Взять дрова", Call("ShedTakeChoppedWood", 1)))
            if _shed_chopped_count > 1:
                items.append(MenuItem("Взять все дрова x{}".format(_shed_chopped_count), Call("ShedTakeChoppedWood", _shed_chopped_count)))

        _carried_lumber = int(player.item_count("lumber_001") or 0)
        if _carried_lumber > 0:
            if _carried_lumber == 1:
                items.append(MenuItem("Сложить бревно в сарае", Call("ShedStoreLumber")))
            else:
                items.append(MenuItem("Сложить бревна в сарае x{}".format(_carried_lumber), Call("ShedStoreLumber")))

        if not shed_has_lumber(room_obj):
            items.append(MenuItem("Сходить в лес за бревнами", [SetDict(rooms.get("Forest").state, "return_target", "Shed"), Call("TravelToForest")]))

        items.append(MenuItem("Вернуться на задний двор", movement_actions("Backyard")))
        return items


label Shed:
    $ renpy.dynamic("_room_desc_rows", "_shed_intro")
    $ rooms.enter("Shed")
    call RoomEnterEventGate(rooms.current_code, False)
    $ scene_runtime.picture = shed_picture() or rooms.current.bg_picture or None
    $ _room_desc_rows = rooms.current.visible_descriptions()
    if len(_room_desc_rows) > 0:
        $ _shed_intro = str(_room_desc_rows[0].text or "")
    else:
        $ _shed_intro = "Сарай."
    $ scene_runtime.text = build_shed_description(True, _shed_intro)
    $ scene_runtime.location_text = scene_runtime.text
    $ rooms.get("Shed").state["notice_pending"] = False
    $ rooms.current.mark_visited()
    $ main_ui_runtime.action_title = "Сарай"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = build_shed_action_items()
    while True:
        call screen main_ui


label ShedStoreLumber:
    $ renpy.dynamic("_shed_lumber_count", "_shed_added_lumber", "_shed_lumber_unit", "_shed_chore_count")
    $ _shed_lumber_count = int(player.item_count("lumber_001") or 0)
    if _shed_lumber_count <= 0:
        $ scene_runtime.text = "У вас нет бревен, которые можно сложить в сарае."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_items = build_shed_action_items()
        return

    $ _shed_added_lumber = 0
    python:
        for _shed_lumber_unit in range(_shed_lumber_count):
            if not player.remove_item("lumber_001", 1):
                break
            if _room_add_item_by_id(rooms.current, "lumber_001"):
                _shed_added_lumber += 1
            else:
                player.add_item("lumber_001", 1)
                break
    if _shed_added_lumber > 0:
        python:
            for _shed_chore_count in range(int(_shed_added_lumber or 0)):
                _pc_register_chore_success("bring_woods")
        if _shed_added_lumber == 1:
            $ rooms.get("Shed").state["notice_text"] = "Вы заносите бревно в сарай и складываете его к остальным запасам."
        else:
            $ rooms.get("Shed").state["notice_text"] = "Вы заносите {} бревна в сарай и складываете их в общую кучу.".format(_shed_added_lumber)
        $ rooms.get("Shed").state["notice_pending"] = True
        $ scene_runtime.text = build_shed_description(True, "")
    else:
        $ scene_runtime.text = "Сейчас не получается сложить бревна в сарае."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = build_shed_action_items()
    return


label ShedTakeChoppedWood(quantity=1):
    $ renpy.dynamic("_shed_take_limit", "_shed_taken_count", "_shed_take_index")
    $ _shed_take_limit = max(1, int(quantity or 1))
    $ _shed_taken_count = 0
    python:
        for _shed_take_index in range(_shed_take_limit):
            if not _room_remove_item_by_id(rooms.get("Shed"), "chopped_wood_001"):
                break
            player.add_item("chopped_wood_001", 1)
            _shed_taken_count += 1
    if _shed_taken_count <= 0:
        $ rooms.get("Shed").state["notice_text"] = "В сарае уже нет колотых дров."
    elif _shed_taken_count == 1:
        $ rooms.get("Shed").state["notice_text"] = "Вы берете одну охапку колотых дров. При себе теперь: {}.".format(int(player.item_count("chopped_wood_001") or 0))
    else:
        $ rooms.get("Shed").state["notice_text"] = "Вы берете {} охапки колотых дров. При себе теперь: {}.".format(_shed_taken_count, int(player.item_count("chopped_wood_001") or 0))
    $ rooms.get("Shed").state["notice_pending"] = True
    $ scene_runtime.text = build_shed_description(True, "")
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = build_shed_action_items()
    call stat
    return


label ShedExamine:
    if not bool(rooms.get("Shed").state["bucket_found"]) and player.item_count("bucket_001") <= 0:
        $ rooms.get("Shed").state["bucket_found"] = True
        $ player.add_item("bucket_001", 1)
        $ scene_runtime.text = "Вы внимательно осматриваете сарай и, пошарив под старыми досками и тряпьем, находите крепкое хозяйственное ведро."
    else:
        $ scene_runtime.text = build_shed_description(False, "Вы внимательно осматриваете сарай.")
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = build_shed_action_items()
    return
