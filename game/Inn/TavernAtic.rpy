init 6 python:
    def tavern_atic_search_available():
        return int(AtticLootFound or 0) == 0

    def tavern_atic_supply_search_available():
        return int(AtticLootFound or 0) == 1 and int(AtticSupplyLootFound or 0) == 0

    def tavern_atic_visible_items():
        items = []
        for row in list(getattr(TavernAticRoom, "game_items", []) or []):
            item_obj = row
            if isinstance(row, str):
                item_obj = get_game_item(row, TavernAticRoom)
            if item_obj is None:
                continue
            if hasattr(item_obj, "is_visible") and not item_obj.is_visible():
                continue
            items.append(item_obj)
        return items

    TavernAticRoom = Room(
        code_name="TavernAtic",
        display_name="Чердак",
        bg_picture="images/tavern/myroom/playr_room attic.png",
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
        npcs=[],
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[0, 1, 2, 3, 4]),
        custom_properties={},
    )


label TavernAtic:
    call EnterLocation("TavernAtic")
    $ CurrentRoom = TavernAticRoom
    $ CurLoc = "TavernAtic"
    $ location = CurLoc
    $ scene_image = attic_room_picture_path() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    else:
        $ _layout_last_picture = ""
    $ MainTxt = TavernAticRoom.descriptions[0].text
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    jump TavernAticView


label TavernAticView:
    show screen main_ui
    $ renpy.pause(hard=True)
    jump TavernAticView


label TavernAticBuildActions:
    $ current_action_title = "Чердак"
    $ current_action_content = None
    $ current_action_items = []
    if tavern_atic_search_available():
        $ current_action_items.append(MenuItem("Порыться в старом хламе", Call("TavernAticSearch")))
    elif tavern_atic_supply_search_available():
        $ current_action_items.append(MenuItem("Порыться в старом хламе еще раз", Call("TavernAticSupplySearch")))
    if player_has_attic_manageable_items():
        $ current_action_items.append(MenuItem("Проверить свои вещи", Call("AtticInventoryMenu", "attic", "TavernAtic")))
    python:
        for _atic_item in tavern_atic_visible_items():
            current_action_items.append(MenuItem(_atic_item.name, Call("TavernAticObjectMenu", _atic_item.object_id)))
        for _exit in TavernAticRoom.visible_exits():
            current_action_items.append(MenuItem(_exit.label, Call("AdvanceMovementTime", _exit.target)))
    return


label TavernAticSearch:
    if int(AtticLootFound or 0) == 0:
        $ AtticLootFound = 1
        python:
            for _loot_id in ("recipe_book_001", "rusty_hunter_rifle_001", "old_leather_cuirass_001"):
                if not _room_has_item_by_id(TavernAticRoom, _loot_id):
                    _room_add_item_by_id(TavernAticRoom, _loot_id)
        $ MainTxt = "Вы долго роетесь среди ящиков, тряпья и обломков мебели. В дальнем углу под кучей пыли находятся {b}очень старая книга с рецептами{/b}, {b}ржавая охотничья винтовка-арбалет{/b} и {b}старый кожаный кирас{/b}."
    else:
        $ MainTxt = "Вы снова шевелите старый хлам, но больше ничего ценного не обнаруживаете."
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    return


label TavernAticSupplySearch:
    if int(AtticSupplyLootFound or 0) == 0:
        $ AtticSupplyLootFound = 1
        $ _player_add_item_by_id("droplets_001", 5)
        $ _player_add_item_by_id("gunpowder_001", 5)
        $ MainTxt = "Вы снова перетряхиваете старый хлам и в дальнем ящике находите завернутые в промасленную тряпку припасы: {b}дробь{/b} и {b}порох{/b}. Этого хватит примерно на пять хороших выстрелов."
    else:
        $ MainTxt = "После второго тщательного обыска чердак больше ничем полезным не радует."
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    return


label TavernAticObjectMenu(object_id=""):
    $ _atic_item = get_game_item(object_id, TavernAticRoom)
    if _atic_item is None or not _room_has_item_by_id(TavernAticRoom, object_id):
        call TavernAticBuildActions
        return
    $ scene_image = attic_item_picture_path(object_id) or attic_room_picture_path() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ MainTxt = str(_atic_item.description or "")
    $ CurLocDesc = MainTxt
    $ current_action_title = str(_atic_item.name or "Чердак")
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _atic_action in _atic_item.visible_actions():
            _atic_args = tuple(getattr(_atic_action, "args", ()) or ())
            if _atic_action.hook == "text":
                current_action_items.append(MenuItem(_atic_action.label, Call("TavernAticObjectText", object_id, _atic_action.action_id)))
            elif _atic_action.hook == "call" and str(_atic_action.target or "") != "":
                current_action_items.append(MenuItem(_atic_action.label, Call(_atic_action.target, *_atic_args)))
            elif _atic_action.hook == "jump" and str(_atic_action.target or "") != "":
                current_action_items.append(MenuItem(_atic_action.label, Jump(_atic_action.target)))
    $ current_action_items.append(MenuItem("Назад", Call("TavernAticRestore")))
    return


label TavernAticObjectText(object_id="", action_id=""):
    python:
        _atic_text = ""
        _atic_item = get_game_item(object_id, TavernAticRoom)
        if _atic_item is not None:
            for _atic_action in _atic_item.visible_actions():
                if getattr(_atic_action, "action_id", "") == str(action_id or ""):
                    _atic_text = str(_atic_action.target or "")
                    break
        if _atic_text:
            MainTxt = _atic_text
            CurLocDesc = _atic_text
    call TavernAticObjectMenu(object_id)
    return


label TavernAticRestore:
    $ scene_image = attic_room_picture_path() or CurrentRoom.bg_picture or None
    if scene_image:
        $ _layout_last_picture = scene_image
    $ MainTxt = TavernAticRoom.descriptions[0].text
    if int(AtticLootFound or 0) == 1:
        $ MainTxt = MainTxt + "\n\nВы уже перерыли здесь хлам и теперь знаете, где лежат найденные вещи."
    $ CurLocDesc = MainTxt
    call TavernAticBuildActions
    return
