# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE: THE STRUCTURE, THE MECHANICS. THE WORDING OF CODE BASE FILE WITHOUT EXPLICIT PERMISSION IN in your request for a change, YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    PLAYER_ROOM_IMAGE = {
        "room": "images/player_room/player_room.png",
        "table": "images/player_room/player_table.png",
        "rifle": "images/player_room/rifle0.png",
        "rifle_loaded": "images/player_room/rifle1.png",
        "wake_up": "images/player_room/wake_up.png",
        "from_bed": "images/player_room/from_bed.png",
        "attic": "images/player_room/player_room_attic.png",
        "door": "images/player_room/player room_door.png",
    }

    def player_room_image_path(image_key="room"):
        return str(PLAYER_ROOM_IMAGE.get(str(image_key or "room").strip(), PLAYER_ROOM_IMAGE["room"]) or "")

    def tavern_my_room_dress_short_name(dress_code=""):
        code = str(dress_code or "").strip()
        try:
            names = ShortDressName
        except Exception:
            names = {}
        if not isinstance(names, dict):
            names = {}
        return str(names.get(code, code) or code).lower()

    def tavern_my_room_dress_full_desc(dress_code=""):
        code = str(dress_code or "").strip()
        try:
            full_descs = FullDressDesc
        except Exception:
            full_descs = {}
        try:
            descs = DressDesc
        except Exception:
            descs = {}
        if not isinstance(full_descs, dict):
            full_descs = {}
        if not isinstance(descs, dict):
            descs = {}
        return str(full_descs.get(code, descs.get(code, "")) or "").strip()

    TavernMyRoomRoomDefinition = Room(
        code_name="TavernMyRoom",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Моя комната",
        bg_picture=player_room_image_path("room"),
        descriptions=[
            RoomDescription(
                text="Это ваша комната. Она невелика и обставленна довольно скромно, большую ее часть занимает кровать. В дальнем углу, у маленького окошка, располагается ларь с вашей одеждой. Других предметов обстановки в ней нет.",
                priority=100,
            ),
        ],
        exits=[
            RoomExit(label="Вернуться в коридор наверху", target="TavernUpstairs"),
        ],
        game_items=[
            "bed_001",
            "chest_001",
            "myroom_window_001",
            "myroom_attic_hatch_001",
        ],
        custom_properties={
            "object_menu_label": "TavernMyRoomObjectMenu",
        },
    )

    def tavern_my_room_get_object(object_id):
        object_key = str(object_id or "").strip()
        room_object = get_game_item(object_key, rooms.get("TavernMyRoom"))
        if room_object is not None:
            return room_object
        return get_game_object(object_key)

    def tavern_my_room_can_go_forest():
        return not rooms.get("Forest").is_first_visit()

    def tavern_my_room_has_floor_item(item_id):
        return _room_has_item_by_id(rooms.get("TavernMyRoom"), str(item_id or "").strip())

    def tavern_my_room_has_recipe_book_access():
        return tavern_my_room_has_floor_item("recipe_book_001") or player.item_count("recipe_book_001") > 0

    def tavern_my_room_table_link_markup():
        return "{a=call:TavernMyRoomTableMenu}{color=#245b2b}стол{/color}{/a}"

    def tavern_my_room_table_picture():
        if renpy.loadable(player_room_image_path("table")):
            return player_room_image_path("table")
        return str(rooms.get("TavernMyRoom").bg_picture or "")

    def tavern_my_room_dynamic_picture():
        if "amanda" in list(people.ids_at("TavernMyRoom") or []):
            if renpy.loadable(player_room_image_path("from_bed")):
                return player_room_image_path("from_bed")
        if tavern_my_room_has_floor_item("rusty_hunter_rifle_001"):
            rifle_key = "rifle_loaded" if rusty_hunter_rifle_loaded_ammo() else "rifle"
            if renpy.loadable(player_room_image_path(rifle_key)):
                return player_room_image_path(rifle_key)
        if tavern_my_room_has_floor_item("recipe_book_001") and renpy.loadable(player_room_image_path("table")):
            return player_room_image_path("table")
        if int(calendar_v2.time_slot()) == 0 and renpy.loadable(player_room_image_path("wake_up")):
            return player_room_image_path("wake_up")
        return str(rooms.get("TavernMyRoom").bg_picture or "")

    def tavern_my_room_dynamic_text():
        room_rows = rooms.get("TavernMyRoom").visible_descriptions()
        if len(room_rows) > 0:
            base_text = str(room_rows[0].text or "")
        else:
            base_text = "Это ваша комната."

        table_markup = tavern_my_room_table_link_markup()
        if table_markup not in base_text:
            base_text += "\n\nУ стены стоит " + table_markup + ", за которым можно читать записи и мастерить полезные вещи."

        extra_rows = []
        if tavern_my_room_has_floor_item("recipe_book_001"):
            extra_rows.append("На небольшом столике у стены лежит старая пыльная книга с рецептами, которую вы сняли с чердака.")
        if tavern_my_room_has_floor_item("rusty_hunter_rifle_001"):
            _rifle_name = str(runtime_item_display_name("rusty_hunter_rifle_001") or "оружие")
            extra_rows.append("В углу у стены прислонена {}. Пускай она и старая, но вид у нее все еще внушительный.".format(_rifle_name))
        if tavern_my_room_has_floor_item("old_leather_cuirass_001"):
            _cuirass_name = str(runtime_item_display_name("old_leather_cuirass_001") or "кираса")
            extra_rows.append("У стены аккуратно оставлена {}. Кожа потемнела от времени, но вещь все еще выглядит крепкой.".format(_cuirass_name))
        if Melissa.temp_room_active("TavernMyRoom"):
            extra_rows.append("Пока в комнате Мелиссы под крышей все еще живет дрянь, часть ее вещей лежит и у вас. Похоже, по ночам она действительно рассчитывает на это убежище.")
        werecat_text = werecat_visible_text("TavernMyRoom")
        if str(werecat_text or "").strip():
            extra_rows.append(str(werecat_text or "").strip())
        if "amanda" in list(people.ids_at("TavernMyRoom") or []):
            extra_rows.append("Аманда сейчас в вашей комнате.")
        if str(player.intimacy.wake_state_notice or "").strip() and int(player.intimacy.morning_arousal_day or -1) == current_game_day():
            extra_rows.append(str(player.intimacy.wake_state_notice or ""))

        if len(extra_rows) > 0:
            return base_text + "\n" + "\n".join(extra_rows)
        return base_text

    def tavern_my_room_scene_state():
        picture_path = tavern_my_room_dynamic_picture()
        room_text = tavern_my_room_dynamic_text()
        return picture_path, room_text

    def tavern_my_room_action_items():
        sections = rooms.get("TavernMyRoom").build_menu_sections()
        items = list(sections["movement"])
        items.extend(travel_to_forest_actions("TavernMyRoom"))
        for item_id in ("rusty_hunter_rifle_001", "old_leather_cuirass_001"):
            if _room_has_item_by_id(rooms.get("TavernMyRoom"), item_id):
                item_obj = get_game_item(item_id, rooms.get("TavernMyRoom"))
                if item_obj is not None:
                    items.append(MenuItem(str(runtime_item_display_name(item_id) or item_id), Call("TavernMyRoomObjectMenu", item_id)))
        items.extend(list(sections["actions"]))
        return items

label TavernMyRoom:
    $ rooms.enter("TavernMyRoom")
    call RoomEnterEventGate(rooms.current_code, False)
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ main_ui_runtime.girl_key = ""
    $ main_ui_runtime.object_id = ""
    $ player_apply_morning_state("TavernMyRoom")
    $ _my_room_picture, _my_room_text = tavern_my_room_scene_state()
    $ scene_runtime.picture = _my_room_picture or None
    if _my_room_picture:
        $ scene_runtime.picture = _my_room_picture
    $ scene_runtime.text = _my_room_text
    $ scene_runtime.location_text = _my_room_text
    $ rooms.current.mark_visited()
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_my_room_action_items()
    while True:
        call screen main_ui


label TavernMyRoomObjectMenu(object_id="", display_text=""):
    $ renpy.dynamic("_room_object", "_default_picture", "_object_picture", "_room_action", "_room_args", "_room_floor_item", "_takeable_floor_item")
    if str(object_id or "") != "":
        $ main_ui_runtime.object_id = str(object_id or "")
    $ object_id = str(main_ui_runtime.object_id or "")
    $ _room_object = tavern_my_room_get_object(object_id)
    if _room_object is None:
        $ main_ui_runtime.action_items = tavern_my_room_action_items()
        return
    if str(display_text or "") != "":
        $ scene_runtime.text = str(display_text or "")
        $ scene_runtime.location_text = scene_runtime.text
    else:
        $ scene_runtime.text = str(_room_object.description or "")
        $ scene_runtime.location_text = scene_runtime.text
    python:
        _object_picture = str(getattr(_room_object, "picture", "") or "").strip()
        if _object_picture and renpy.loadable(_object_picture):
            scene_runtime.picture = _object_picture
        else:
            _default_picture = tavern_my_room_dynamic_picture()
            scene_runtime.picture = _default_picture or None
            if _default_picture:
                scene_runtime.picture = _default_picture
    $ main_ui_runtime.action_title = str(_room_object.name or "Действия")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        _room_floor_item = _room_has_item_by_id(rooms.get("TavernMyRoom"), object_id)
        _takeable_floor_item = _room_floor_item and object_id in ("recipe_book_001", "rusty_hunter_rifle_001", "old_leather_cuirass_001")
        for _room_action in _room_object.visible_actions():
            _room_args = tuple(getattr(_room_action, "args", ()) or ())
            if _room_action.hook == "text":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call("TavernMyRoomObjectText", object_id, _room_action.action_id)))
            elif not _takeable_floor_item and _room_action.hook == "call" and str(_room_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif not _takeable_floor_item and _room_action.hook == "jump" and str(_room_action.target or "") != "":
                main_ui_runtime.action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        if _takeable_floor_item:
            if object_id == "recipe_book_001":
                main_ui_runtime.action_items.append(MenuItem("Сесть за стол", Call("TavernMyRoomTableMenu")))
            main_ui_runtime.action_items.append(MenuItem("Взять", Call("TavernMyRoomTakeFloorItem", object_id)))
        main_ui_runtime.action_items.append(MenuItem("Назад", [
            SetField(scene_runtime, "text", tavern_my_room_dynamic_text()),
            SetField(scene_runtime, "location_text", tavern_my_room_dynamic_text()),
            SetField(main_ui_runtime, "action_title", "Ваша комната"),
            SetField(main_ui_runtime, "action_content", None),
            SetField(main_ui_runtime, "action_items", tavern_my_room_action_items()),
            Function(main_ui_restart_interaction),
        ]))
    $ renpy.restart_interaction()
    return


label TavernMyRoomObjectText(object_id="", action_id=""):
    $ renpy.dynamic("_room_text", "_room_name", "_room_object", "_room_action")
    python:
        _room_text = ""
        _room_name = ""
        _room_object = tavern_my_room_get_object(object_id)
        if _room_object is not None:
            _room_name = str(getattr(_room_object, "name", "") or "")
            for _room_action in _room_object.visible_actions():
                if getattr(_room_action, "action_id", "") == str(action_id or ""):
                    _room_text = str(_room_action.target or "")
                    break
        if _room_text:
            scene_runtime.text = _room_text
            scene_runtime.location_text = _room_text
            main_ui_runtime.action_title = _room_name or "Действия"
    call TavernMyRoomObjectMenu(object_id, _room_text)
    return


label TavernMyRoomTakeFloorItem(item_id=""):
    $ renpy.dynamic("_item_id", "_take_result")
    $ _item_id = str(item_id or "").strip()
    $ _take_result = take(rooms.get("TavernMyRoom"), _item_id)
    $ main_ui_runtime.action_items = tavern_my_room_action_items()
    $ scene_runtime.text = str((_take_result or {}).get("text", "") or "Вы забираете вещь.")
    $ scene_runtime.location_text = scene_runtime.text
    $ renpy.restart_interaction()
    return


label TavernMyRoomOpenChest(preserve_text=False):
    $ renpy.dynamic("_room_object", "_all_dresses", "_appearance", "_current_dress", "_dress", "_dress_key", "_short")
    $ _room_object = tavern_my_room_get_object("chest_001")
    $ player_ensure_nightwear_in_chest()
    if _room_object is not None:
        $ _room_object.state["open"] = 1
    if not bool(preserve_text):
        $ scene_runtime.text = "Вы открываете ларь. Внутри хранится ваша одежда."
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Ларь"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        _all_dresses = []
        _appearance = player.appearance
        for _dress in list(_appearance.owned_dresses or []):
            _dress_key = str(_dress or "").strip()
            if _dress_key and _dress_key not in _all_dresses:
                _all_dresses.append(_dress_key)
        _current_dress = str(_appearance.current_dress or "").strip()
        if _current_dress and _appearance.has_dress(_current_dress) and _current_dress not in _all_dresses:
            _all_dresses.append(_current_dress)
        if len(_all_dresses) <= 0 and not bool(preserve_text):
            scene_runtime.text = "В ларе пока пусто."
            scene_runtime.location_text = scene_runtime.text
        else:
            for _dress in _all_dresses:
                _short = tavern_my_room_dress_short_name(_dress)
                if _dress != _current_dress:
                    main_ui_runtime.action_items.append(MenuItem("Надеть " + _short, Call("TavernMyRoomWearDress", _dress)))
                    if player_can_tear_wardrobe_dress(_dress):
                        main_ui_runtime.action_items.append(MenuItem("Порвать " + _short + " на лоскуты", Call("TavernMyRoomTearDressToCloth", _dress)))
                else:
                    main_ui_runtime.action_items.append(MenuItem("Снять " + _short, Call("TavernMyRoomRemoveDress", _dress)))
        if not player_is_naked():
            main_ui_runtime.action_items.append(MenuItem("Раздеться для сна", Call("TavernMyRoomSetSleepLayer", "nothing")))
    $ main_ui_runtime.action_items.append(MenuItem("Закрыть ларь", Call("TavernMyRoomCloseChest")))
    $ renpy.restart_interaction()
    return


label TavernMyRoomCloseChest:
    $ renpy.dynamic("_room_object")
    $ _room_object = tavern_my_room_get_object("chest_001")
    if _room_object is not None:
        $ _room_object.state["open"] = 0
    $ _my_room_picture, _my_room_text = tavern_my_room_scene_state()
    $ scene_runtime.picture = _my_room_picture or None
    if _my_room_picture:
        $ scene_runtime.picture = _my_room_picture
    $ scene_runtime.text = _my_room_text
    $ scene_runtime.location_text = _my_room_text
    $ main_ui_runtime.action_title = "Действия"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = tavern_my_room_action_items()
    $ renpy.restart_interaction()
    return


label TavernMyRoomSleepAction:
    if str(player.appearance.sleep_bottom_layer or "") == "daywear":
        $ player_set_sleep_layer("nightwear")
    call Sleep("TavernMyRoom", 1, "Вы ложитесь на кровать и быстро проваливаетесь в сон.", "TavernMyRoom", "bed_001")


label TavernMyRoomSetSleepLayer(mode="daywear"):
    $ renpy.dynamic("_sleep_mode")
    $ _sleep_mode = player_set_sleep_layer(mode)
    if _sleep_mode == "nightwear":
        $ scene_runtime.text = "Вы надеваете ночную рубашку из ларя. Для сна этого достаточно."
    elif _sleep_mode == "nothing":
        if str(mode or "").strip().lower() in ("night", "nightwear", "sleep"):
            $ scene_runtime.text = "В ларе нет ночной рубашки. Придется спать без нее."
        else:
            $ scene_runtime.text = "Вы снимаете одежду и оставляете ее в ларе. Для сна так удобно, но дальше второго этажа в таком виде идти нельзя."
    else:
        $ scene_runtime.text = "Вы приводите себя в порядок и надеваете одежду из ларя."
    $ scene_runtime.location_text = scene_runtime.text
    call TavernMyRoomOpenChest(True)
    return


label TavernMyRoomTableMenu:
    $ renpy.dynamic("_default_picture", "_table_picture")
    if not tavern_my_room_has_recipe_book_access():
        $ _default_picture = tavern_my_room_dynamic_picture()
        $ scene_runtime.picture = _default_picture or None
        if _default_picture:
            $ scene_runtime.picture = _default_picture
        $ scene_runtime.text = "Вам сейчас нечем здесь заняться."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = "Стол"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = [MenuItem("Назад", Jump("TavernMyRoom"))]
    else:
        $ _table_picture = tavern_my_room_table_picture()
        $ scene_runtime.picture = _table_picture or None
        if _table_picture:
            $ scene_runtime.picture = _table_picture
        if tavern_my_room_has_floor_item("recipe_book_001"):
            $ scene_runtime.text = "На столе уже лежит старая книга с рецептами. Здесь можно спокойно читать записи и сразу пробовать что-нибудь мастерить."
        else:
            $ scene_runtime.text = "Вы раскладываете на столе книгу с рецептами, ингредиенты и всякую мелочь для нехитрой работы руками. Отсюда удобно и читать записи, и сразу что-нибудь мастерить."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = "Стол"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = []
        $ main_ui_runtime.action_items.append(MenuItem("Читать книгу рецептов", Call("TavernMyRoomTableRead")))
        $ main_ui_runtime.action_items.append(MenuItem("Создать предмет", Call("TavernMyRoomTableCraftMenu")))
        $ main_ui_runtime.action_items.append(MenuItem("Назад", Jump("TavernMyRoom")))
    $ renpy.restart_interaction()
    return



label TavernMyRoomTableRead(recipe_id=""):
    $ renpy.dynamic("_table_recipe_id", "_table_picture", "_page", "_recipe_id", "_title")
    if not tavern_my_room_has_recipe_book_access():
        call TavernMyRoomTableMenu
        return
    $ recipe_book_item_state()["read_count"] = max(0, int(recipe_book_item_state().get("read_count", 0) or 0)) + 1
    $ _table_recipe_id = str(recipe_id or recipe_book_resolved_selected_id() or "").strip()
    $ _table_picture = recipe_page_image_path(_table_recipe_id) or tavern_my_room_table_picture()
    $ scene_runtime.picture = _table_picture or None
    if _table_picture:
        $ scene_runtime.picture = _table_picture
    if len(list(visible_recipe_pages() or [])) <= 0:
        $ scene_runtime.text = "Вы раскрываете записи на столе, но пока не можете разобрать ни одного полезного рецепта."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = "Рецепты"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = [MenuItem("Назад к столу", Call("TavernMyRoomTableMenu"))]
        return
    $ scene_runtime.text = recipe_book_page_text(_table_recipe_id)
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = recipe_book_selected_title(_table_recipe_id)
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        for _recipe_id in list(visible_recipe_pages() or []):
            _page = recipe_catalog.get(_recipe_id)
            if _page is None:
                continue
            _title = str(getattr(_page, "title", _recipe_id) or _recipe_id)
            if str(_recipe_id or "") == str(_table_recipe_id or ""):
                _title += " (открыто)"
            main_ui_runtime.action_items.append(MenuItem(_title, Call("TavernMyRoomTableRead", _recipe_id)))
        if recipe_book_can_notice_hidden_note():
            main_ui_runtime.action_items.append(MenuItem("Достать тонкую вкладку между страницами", Call("RecipeBookFindTinyNote", "TavernMyRoom", "recipe_book_001", "table")))
        elif bool(recipe_book_item_state().get("tiny_note_found", False)) and not recipe_book_hidden_recipes_revealed():
            main_ui_runtime.action_items.append(MenuItem("Нагреть пергамент и смазать вином", Call("RecipeBookRevealHiddenRecipes", "TavernMyRoom", "recipe_book_001", "table")))
    $ main_ui_runtime.action_items.append(MenuItem("Назад к столу", Call("TavernMyRoomTableMenu")))
    $ renpy.restart_interaction()
    return


label TavernMyRoomTableCraftMenu:
    $ renpy.dynamic("_table_picture", "_craftable_count", "_page", "_recipe_id")
    if not tavern_my_room_has_recipe_book_access():
        call TavernMyRoomTableMenu
        return
    $ _table_picture = tavern_my_room_table_picture()
    $ scene_runtime.picture = _table_picture or None
    if _table_picture:
        $ scene_runtime.picture = _table_picture
    $ scene_runtime.text = "Вы раскладываете на столе все, что может пригодиться для работы, и прикидываете, что можно сделать прямо сейчас."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Верстак"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ _craftable_count = 0
    python:
        for _recipe_id in list(craftable_recipe_pages() or []):
            _page = recipe_catalog.get(_recipe_id)
            if _page is None:
                continue
            _craftable_count += 1
            main_ui_runtime.action_items.append(MenuItem("Сделать: " + recipe_result_display_name(_recipe_id), Call("TavernMyRoomTableCraftItem", _recipe_id)))
    if int(_craftable_count or 0) <= 0:
        $ scene_runtime.text = scene_runtime.text + "\n\nСейчас ни один рецепт не готов полностью. Откройте нужную запись, чтобы проверить, чего не хватает."
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items.append(MenuItem("Назад к столу", Call("TavernMyRoomTableMenu")))
    return


label TavernMyRoomTableCraftItem(recipe_id=""):
    $ renpy.dynamic("_table_recipe_id", "_craft_result", "_craft_picture")
    $ _table_recipe_id = str(recipe_id or "").strip()
    $ _craft_result = apply_recipe_craft(_table_recipe_id)
    if str(_table_recipe_id or "") == "soap_recipe" and backyard_has_ash_barrel():
        $ _craft_picture = "images/tavern/backyard/soap_backyard.png"
    else:
        $ _craft_picture = tavern_my_room_table_picture()
    $ scene_runtime.picture = _craft_picture or None
    if _craft_picture:
        $ scene_runtime.picture = _craft_picture
    if bool(_craft_result.get("ok", False)):
        $ scene_runtime.text = str(_craft_result.get("text", "") or "Вы мастерите новую вещь по рецепту.")
    else:
        $ scene_runtime.text = str(_craft_result.get("text", "") or "Сейчас для этого дела не хватает нужных вещей.")
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Верстак"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [
        MenuItem("Продолжить работу", Call("TavernMyRoomTableCraftMenu")),
        MenuItem("Читать записи", Call("TavernMyRoomTableRead", _table_recipe_id)),
        MenuItem("Назад к столу", Call("TavernMyRoomTableMenu")),
    ]
    return


label TavernMyRoomWearDress(dress_code=""):
    $ renpy.dynamic("_dress", "_short", "_desc")
    $ _dress = str(dress_code or "")
    if _dress != "":
        $ _short = tavern_my_room_dress_short_name(_dress)
        $ _desc = tavern_my_room_dress_full_desc(_dress)
        if player.appearance.wear_dress(_dress, current_game_day()):
            call stat
            if _desc:
                $ scene_runtime.text = "Вы надели %s. %s" % (str(_short), str(_desc))
            else:
                $ scene_runtime.text = "Вы надели %s." % str(_short)
        else:
            $ scene_runtime.text = "Этой одежды уже нет в ларе."
        $ scene_runtime.location_text = scene_runtime.text
    call TavernMyRoomOpenChest
    return


label TavernMyRoomRemoveDress(dress_code=""):
    $ renpy.dynamic("_dress", "_short")
    $ _dress = str(dress_code or "").strip()
    if _dress != "" and _dress == str(player.appearance.current_dress or "").strip():
        $ player.appearance.remove_current_dress(_dress)
        call stat
        $ _short = tavern_my_room_dress_short_name(_dress)
        $ scene_runtime.text = "Вы сняли %s и положили в ларь." % str(_short)
        $ scene_runtime.location_text = scene_runtime.text
    else:
        $ scene_runtime.text = "Сейчас эта одежда на вас не надета."
        $ scene_runtime.location_text = scene_runtime.text
    call TavernMyRoomOpenChest(True)
    return


label TavernMyRoomTearDressToCloth(dress_code=""):
    $ renpy.dynamic("_tear_result")
    $ _tear_result = player_tear_wardrobe_dress(dress_code)
    $ scene_runtime.text = str((_tear_result or {}).get("text", "") or "Вы откладываете одежду в сторону.")
    $ scene_runtime.location_text = scene_runtime.text
    call TavernMyRoomOpenChest(True)
    return
