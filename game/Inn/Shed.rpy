# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default ShedNoticeText = ""
default ShedNoticePending = False
default ShedBucketFound = 0

default ShedNoticeText = ""
default ShedNoticePending = False
default ShedBucketFound = 0

default ShedNoticeText = ""
default ShedNoticePending = False
default ShedBucketFound = 0

init 6 python:
    ShedRoom = Room(
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
    )

    def shed_has_lumber(room_obj=None):
        target_room = room_obj if room_obj is not None else CurrentRoom
        if target_room is None:
            target_room = ShedRoom
        return _room_has_item_by_id(target_room, "lumber_001")

    def shed_picture():
        current_minutes = (int(calendar_v2.hour or 0) % 24) * 60 + int(calendar_v2.minute or 0)
        if 360 <= current_minutes <= 1170:
            return "images/tavern/backyard/shed/shed.png"
        return "images/tavern/backyard/shed/shed_night.png"

    def build_shed_description(include_notice=True, intro_text=""):
        room_obj = CurrentRoom if CurrentRoom is not None else ShedRoom
        room_item_ids = [get_object_id(row) for row in list(getattr(room_obj, "game_items", []) or [])]
        text_parts = []

        intro_value = str(intro_text or "").strip()
        if intro_value:
            text_parts.append(intro_value)

        if include_notice and bool(ShedNoticePending) and str(ShedNoticeText or "").strip():
            text_parts.append(str(ShedNoticeText or "").strip())

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
        elif _player_has_item_by_id("old_axe_001") and player_has_equipped_weapon("old_axe_001"):
            text_parts.append("{} заткнут у вас за пояс.".format(axe_name[:1].upper() + axe_name[1:]))
        elif _player_has_item_by_id("old_axe_001"):
            text_parts.append("{} лежит у вас в сумке.".format(axe_name[:1].upper() + axe_name[1:]))
        else:
            text_parts.append("Крючок для топора пуст.")

        return "\n\n".join([row for row in text_parts if str(row or "").strip()])

    def build_shed_action_items():
        room_obj = CurrentRoom if CurrentRoom is not None else ShedRoom
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
            items.append(MenuItem("Сходить в лес за бревнами", Call("TravelToForest", "Shed")))

        items.append(MenuItem("Вернуться на задний двор", Call("AdvanceMovementTime", "Backyard")))
        return items


label Shed:
    $ CurrentRoom = ShedRoom
    $ CurLoc = "Shed"
    call RoomEnterEventGate(CurLoc, False)
    $ scene_image = shed_picture() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ _room_desc_rows = CurrentRoom.visible_descriptions()
    if len(_room_desc_rows) > 0:
        $ _shed_intro = str(_room_desc_rows[0].text or "")
    else:
        $ _shed_intro = "Сарай."
    $ MainTxt = build_shed_description(True, _shed_intro)
    $ CurLocDesc = MainTxt
    $ ShedNoticePending = False
    $ CurrentRoom.mark_visited()
    $ current_action_title = "Сарай"
    $ current_action_content = None
    call ShedRoomActions
    while True:
        call ShedRoomActions
    $ _shed_ui_return = None
    while _shed_ui_return is None:
        $ _shed_ui_return = None
    while _shed_ui_return is None:
        call screen main_ui
        $ _shed_ui_return = _return
    jump Shed


label ShedRoomActions:
    $ current_action_title = "Сарай"
    $ current_action_content = None
    $ current_action_items = build_shed_action_items()
        $ _shed_ui_return = _return
    jump Shed


label ShedRoomActions:


label ShedStoreLumber:
    $ _shed_lumber_count = int(player.item_count("lumber_001") or 0)
    if _shed_lumber_count <= 0:
        $ MainTxt = "У вас нет бревен, которые можно сложить в сарае."
        $ CurLocDesc = MainTxt
        call ShedRoomActions
        return

    $ _shed_added_lumber = 0
    python:
        for _shed_lumber_unit in range(_shed_lumber_count):
            if not player.remove_item("lumber_001", 1):
                break
            if _room_add_item_by_id(CurrentRoom, "lumber_001"):
                _shed_added_lumber += 1
            else:
                player.add_item("lumber_001", 1)
                break
    if _shed_added_lumber > 0:
        python:
            for _shed_chore_count in range(int(_shed_added_lumber or 0)):
                _pc_register_chore_success("bring_woods")
        if _shed_added_lumber == 1:
            $ ShedNoticeText = "Вы заносите бревно в сарай и складываете его к остальным запасам."
        else:
            $ ShedNoticeText = "Вы заносите {} бревна в сарай и складываете их в общую кучу.".format(_shed_added_lumber)
        $ ShedNoticePending = True
        $ MainTxt = build_shed_description(True, "")
    else:
        $ MainTxt = "Сейчас не получается сложить бревна в сарае."
    $ CurLocDesc = MainTxt
    call ShedRoomActions
    return


label ShedTakeChoppedWood(quantity=1):
    $ _shed_take_limit = max(1, int(quantity or 1))
    $ _shed_taken_count = 0
    python:
        for _shed_take_index in range(_shed_take_limit):
            if not _room_remove_item_by_id(ShedRoom, "chopped_wood_001"):
                break
            player.add_item("chopped_wood_001", 1)
            _shed_taken_count += 1
    if _shed_taken_count <= 0:
        $ ShedNoticeText = "В сарае уже нет колотых дров."
    elif _shed_taken_count == 1:
        $ ShedRoom.state["notice_text"] = "Вы берете одну охапку колотых дров. При себе теперь: {}.".format(int(player.item_count("chopped_wood_001") or 0))
    else:
        $ ShedRoom.state["notice_text"] = "Вы берете {} охапки колотых дров. При себе теперь: {}.".format(_shed_taken_count, int(player.item_count("chopped_wood_001") or 0))
    $ ShedRoom.state["notice_pending"] = True
    $ MainTxt = build_shed_description(True, "")
    $ CurLocDesc = MainTxt
    call ShedRoomActions
    call stat
    return


label ShedExamine:
    if not bool(ShedRoom.state["bucket_found"]) and player.item_count("bucket_001") <= 0:
        $ ShedRoom.state["bucket_found"] = True
        $ player.add_item("bucket_001", 1)
        $ MainTxt = "Вы внимательно осматриваете сарай и, пошарив под старыми досками и тряпьем, находите крепкое хозяйственное ведро."
    else:
        $ MainTxt = build_shed_description(False, "Вы внимательно осматриваете сарай.")
    $ CurLocDesc = MainTxt
    call ShedRoomActions
    return
