# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 6 python:
    def tavern_atic_search_available():
        return not bool(rooms.get("TavernAtic").state.get("loot_found", False))

    def tavern_atic_supply_search_available():
        return bool(rooms.get("TavernAtic").state.get("loot_found", False)) and not bool(rooms.get("TavernAtic").state.get("supply_loot_found", False))

    def tavern_atic_visible_items():
        items = []
        seen_item_ids = set()
        for row in list(getattr(rooms.get("TavernAtic"), "game_items", []) or []):
            item_obj = row
            if isinstance(row, str):
                item_obj = get_game_item(row, rooms.get("TavernAtic"))
            if item_obj is None:
                continue
            item_id = str(getattr(item_obj, "object_id", "") or "").strip()
            if item_id in seen_item_ids:
                continue
            if hasattr(item_obj, "is_visible") and not item_obj.is_visible():
                continue
            seen_item_ids.add(item_id)
            items.append(item_obj)
        return items

    def tavern_atic_action_items():
        items = []
        if tavern_atic_search_available():
            items.append(MenuItem("Порыться в старом хламе", Call("TavernAticSearch")))
        elif tavern_atic_supply_search_available():
            items.append(MenuItem("Порыться в старом хламе еще раз", Call("TavernAticSupplySearch")))
        if story_event_available("TavernAtic", "melissa_bats"):
            items.append(MenuItem(Melissa.bat_attic_event_caption(), Call("checkTriggers", "TavernAtic", "melissa_bats", 0)))
        for attic_item in tavern_atic_visible_items():
            item_id = str(getattr(attic_item, "object_id", "") or "")
            item_count = _room_item_count_by_id(rooms.get("TavernAtic"), item_id)
            caption = str(attic_item.name or item_id)
            if item_count > 1:
                caption = "{} x{}".format(caption, item_count)
            items.append(MenuItem(caption, Call("TavernAticObjectMenu", item_id)))
        for room_exit in rooms.get("TavernAtic").visible_exits():
            items.append(MenuItem(room_exit.label, movement_actions(room_exit.target)))
        return items

    TavernAticRoomDefinition = Room(
        code_name="TavernAtic",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Чердак",
        bg_picture="images/player_room/player_room_attic.png",
        descriptions=[
            RoomDescription(
                text="Вы выбираетесь на пыльный чердак трактира. Под самой крышей темно, пахнет старым деревом, сухой пылью и забытыми вещами. Между балками навалены какие-то ящики, тряпье и обломки мебели.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Спуститься обратно в комнату", target="TavernMyRoom"),
        ],
        game_items=[],
        custom_properties={},
        state={
            "loot_found": False,
            "supply_loot_found": False,
        },
    )


label TavernAtic:
    $ rooms.enter("TavernAtic")
    $ scene_runtime.picture = attic_room_picture_path() or rooms.current.bg_picture or None
    $ scene_runtime.text = rooms.get("TavernAtic").descriptions[0].text
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Чердак"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_atic_action_items()
    while True:
        call screen main_ui


label TavernAticSearch:
    $ renpy.dynamic("_loot_id")
    if not bool(rooms.get("TavernAtic").state.get("loot_found", False)):
        $ rooms.get("TavernAtic").state["loot_found"] = True
        python:
            for _loot_id in ("recipe_book_001", "rusty_hunter_rifle_001", "old_leather_cuirass_001"):
                if not _room_has_item_by_id(rooms.get("TavernAtic"), _loot_id):
                    _room_add_item_by_id(rooms.get("TavernAtic"), _loot_id)
        $ scene_runtime.text = "Вы долго роетесь среди ящиков, тряпья и обломков мебели. В дальнем углу под кучей пыли находятся {b}очень старая книга с рецептами{/b}, {b}ржавая охотничья винтовка-арбалет{/b} и {b}старый кожаный кирас{/b}."
    else:
        $ scene_runtime.text = "Вы снова шевелите старый хлам, но больше ничего ценного не обнаруживаете."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = tavern_atic_action_items()
    return


label TavernAticSupplySearch:
    if not bool(rooms.get("TavernAtic").state.get("supply_loot_found", False)):
        $ rooms.get("TavernAtic").state["supply_loot_found"] = True
        $ player.add_item("droplets_001", 5)
        $ player.add_item("gunpowder_001", 5)
        $ scene_runtime.text = "Вы снова перетряхиваете старый хлам и в дальнем ящике находите завернутые в промасленную тряпку припасы: {b}дробь{/b} и {b}порох{/b}. Этого хватит примерно на пять хороших выстрелов. Вы сразу забираете находку с собой."
    else:
        $ scene_runtime.text = "После второго тщательного обыска чердак больше ничем полезным не радует."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items = tavern_atic_action_items()
    return


label TavernAticObjectMenu(object_id=""):
    $ renpy.dynamic("_atic_item")
    $ renpy.dynamic("_atic_action", "_atic_args", "_atic_has_take_action")
    $ _atic_item = get_game_item(object_id, rooms.get("TavernAtic"))
    if _atic_item is None or not _room_has_item_by_id(rooms.get("TavernAtic"), object_id):
        $ main_ui_runtime.action_items = tavern_atic_action_items()
        return
    $ scene_runtime.picture = attic_item_picture_path(object_id) or attic_room_picture_path() or rooms.current.bg_picture or None
    $ scene_runtime.text = str(_atic_item.description or "")
    if _room_item_count_by_id(rooms.get("TavernAtic"), object_id) > 1:
        $ scene_runtime.text = scene_runtime.text + "\n\nЗдесь лежит несколько одинаковых предметов: {}.".format(_room_item_count_by_id(rooms.get("TavernAtic"), object_id))
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = str(_atic_item.name or "Чердак")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        _atic_has_take_action = False
        for _atic_action in _atic_item.visible_actions():
            _atic_args = tuple(getattr(_atic_action, "args", ()) or ())
            if str(getattr(_atic_action, "target", "") or "") == "Take":
                _atic_has_take_action = True
            if _atic_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_atic_action.label, Call("TavernAticObjectText", object_id, _atic_action.action_id)))
            elif _atic_action.hook == "call" and str(_atic_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_atic_action.label, Call(_atic_action.target, *_atic_args)))
            elif _atic_action.hook == "jump" and str(_atic_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_atic_action.label, Jump(_atic_action.target)))
        if bool(getattr(_atic_item, "carriable", False)) and not _atic_has_take_action:
            main_ui_runtime.action_items.append(MenuItem("Взять", Call("Take", object_id, "TavernAtic", "", object_id)))
    $ main_ui_runtime.action_items.append(MenuItem("Назад", [
        SetField(scene_runtime, "picture", attic_room_picture_path() or rooms.get("TavernAtic").bg_picture or None),
        SetField(scene_runtime, "text", rooms.get("TavernAtic").descriptions[0].text),
        SetField(scene_runtime, "location_text", rooms.get("TavernAtic").descriptions[0].text),
        SetField(main_ui_runtime, "action_title", "Чердак"),
        SetField(main_ui_runtime, "action_content", None),
        SetField(main_ui_runtime, "action_items", tavern_atic_action_items()),
        Function(main_ui_restart_interaction),
    ]))
    return


label TavernAticObjectText(object_id="", action_id=""):
    $ renpy.dynamic("_atic_action", "_atic_item", "_atic_text")
    python:
        _atic_text = ""
        _atic_item = get_game_item(object_id, rooms.get("TavernAtic"))
        if _atic_item is not None:
            for _atic_action in _atic_item.visible_actions():
                if getattr(_atic_action, "action_id", "") == str(action_id or ""):
                    _atic_text = str(_atic_action.target or "")
                    break
        if _atic_text:
            scene_runtime.text = _atic_text
            scene_runtime.location_text = _atic_text
    call TavernAticObjectMenu(object_id)
    return

