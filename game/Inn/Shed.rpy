default ShedNoticeText = ""
default ShedNoticePending = False
default ShedBucketFound = 0

init 6 python:
    ShedRoom = Room(
        code_name="Shed",
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
        npcs=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={},
    )

    def shed_has_lumber(room_obj=None):
        target_room = room_obj if room_obj is not None else CurrentRoom
        if target_room is None:
            target_room = ShedRoom
        return _room_has_item_by_id(target_room, "lumber_001")

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
                text_parts.append("В сарае лежат {}. Всего: 1 единица.".format(chopped_name))
            else:
                text_parts.append("В сарае лежат {}. Всего: {} единиц.".format(chopped_name, chopped_count))
        else:
            text_parts.append("Поленница пуста.")

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
        else:
            text_parts.append("{} у вас.".format(axe_name[:1].upper() + axe_name[1:]))

        return "\n\n".join([row for row in text_parts if str(row or "").strip()])

    def build_shed_action_items():
        room_obj = CurrentRoom if CurrentRoom is not None else ShedRoom
        items = [MenuItem("Осмотреть сарай", Call("ShedExamine"))]
        seen_object_ids = set()
        hidden_action_ids = {"examine_lumber", "examine_chopped_wood"}

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

        if _player_has_item_by_id("lumber_001"):
            items.append(MenuItem("Сложить бревно в сарае", Call("Drop", "lumber_001", "Shed", "Вы заносите бревно в сарай и складываете его к остальным запасам.", "lumber_001")))

        if not shed_has_lumber(room_obj):
            items.append(MenuItem("Сходить в лес за бревнами", Call("TravelToForest", "Shed")))

        items.append(MenuItem("Вернуться на задний двор", Call("AdvanceMovementTime", "Backyard")))
        return items


label Shed:
    call EnterLocation("Shed")
    $ CurrentRoom = ShedRoom
    $ CurLoc = "Shed"
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
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
    call ShedRoomActions
    jump ShedView


label ShedView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump ShedView


label ShedRoomActions:
    $ current_action_title = "Сарай"
    $ current_action_content = None
    $ current_action_items = build_shed_action_items()
    return


label ShedExamine:
    if int(ShedBucketFound or 0) == 0 and _player_item_count_by_id("bucket_001") <= 0:
        $ ShedBucketFound = 1
        $ _player_add_item_by_id("bucket_001", 1)
        $ MainTxt = "Вы внимательно осматриваете сарай и, пошарив под старыми досками и тряпьем, находите крепкое хозяйственное ведро."
    else:
        $ MainTxt = build_shed_description(False, "Вы внимательно осматриваете сарай.")
    $ CurLocDesc = MainTxt
    call ShedRoomActions
    return
