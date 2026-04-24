init python:
    TavernMyRoomRoom = Room(
        code_name="TavernMyRoom",
        group_name=ROOM_GROUP_TAVERN,
        display_name="Моя комната",
        bg_picture="bg myroom",
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
        room_object = get_game_item(object_key, TavernMyRoomRoom)
        if room_object is not None:
            return room_object
        return get_game_object(object_key)

    def tavern_my_room_can_go_forest():
        return bool(roomFirstVisit.get("Forest", False))

    def tavern_my_room_has_floor_item(item_id):
        return _room_has_item_by_id(TavernMyRoomRoom, str(item_id or "").strip())

    def tavern_my_room_has_recipe_book_access():
        return tavern_my_room_has_floor_item("recipe_book_001") or _player_item_count_by_id("recipe_book_001") > 0

    def tavern_my_room_table_link_markup():
        return "{a=call:TavernMyRoomTableMenu}{color=#245b2b}стол{/color}{/a}"

    def tavern_my_room_table_picture():
        if renpy.loadable("images/tavern/myroom/player_table.png"):
            return "images/tavern/myroom/player_table.png"
        return str(TavernMyRoomRoom.bg_picture or "")

    def tavern_my_room_dynamic_picture():
        if tavern_my_room_has_floor_item("rusty_hunter_rifle_001"):
            if renpy.loadable("images/tavern/myroom/rifle.png"):
                return "images/tavern/myroom/rifle.png"
            if renpy.loadable("images/tavern/myroom/riffle.png"):
                return "images/tavern/myroom/riffle.png"
        if tavern_my_room_has_floor_item("recipe_book_001") and renpy.loadable("images/tavern/myroom/player_table.png"):
            return "images/tavern/myroom/player_table.png"
        if int(time or 0) == 0 and renpy.loadable("images/tavern/myroom/wake_up_2.png"):
            return "images/tavern/myroom/wake_up_2.png"
        return str(TavernMyRoomRoom.bg_picture or "")

    def tavern_my_room_dynamic_text():
        room_rows = TavernMyRoomRoom.visible_descriptions()
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
        if melissa_temp_room_active("TavernMyRoom"):
            extra_rows.append("Пока в комнате Мелиссы под крышей все еще живет дрянь, часть ее вещей лежит и у вас. Похоже, по ночам она действительно рассчитывает на это убежище.")

        if len(extra_rows) > 0:
            return base_text + "\n" + "\n".join(extra_rows)
        return base_text

    def tavern_my_room_scene_state():
        picture_path = tavern_my_room_dynamic_picture()
        room_text = tavern_my_room_dynamic_text()
        return picture_path, room_text

label TavernMyRoom:
    $ dog_prepare_current_spawn()
    $ CurrentRoom = TavernMyRoomRoom
    $ CurLoc = "TavernMyRoom"
    $ location = CurLoc
    call CheckDailyEvent("", "_story_enter", CurLoc, time)
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ current_action_items = []
    $ current_girl_key = ""
    $ current_object_id = ""
    call LOC("TavernMyRoom")
    $ _my_room_picture, _my_room_text = tavern_my_room_scene_state()
    $ scene_image = _my_room_picture or None
    if _my_room_picture:
        $ _layout_last_picture = _my_room_picture
    $ MainTxt = _my_room_text
    $ CurLocDesc = _my_room_text
    $ CurrentRoom.mark_visited()
    call TavernMyRoomBuildActions
    show screen main_ui
    $ renpy.pause(hard=True)
    return


label TavernMyRoomView:
    show screen main_ui
    $ renpy.pause(hard=True)
    return


label TavernMyRoomBuildActions:
    $ _my_room_picture, _my_room_text = tavern_my_room_scene_state()
    $ scene_image = _my_room_picture or None
    if _my_room_picture:
        $ _layout_last_picture = _my_room_picture
    $ MainTxt = _my_room_text
    $ CurLocDesc = _my_room_text
    $ current_action_title = "Действия"
    $ current_action_content = None
    $ room_menu = CurrentRoom.build_menu_sections()
    $ current_action_items = list(room_menu["movement"])
    if tavern_my_room_can_go_forest():
        $ current_action_items.append(MenuItem("Идти в лес", Call("TravelToForest", "TavernMyRoom")))
    if dog_is_available_here("TavernMyRoom"):
        $ current_action_items.append(MenuItem(dog_room_action_caption("TavernMyRoom"), Call("IntDogTalk", "TavernMyRoom")))
    python:
        for _room_item_id in ("recipe_book_001", "rusty_hunter_rifle_001", "old_leather_cuirass_001"):
            if _room_has_item_by_id(TavernMyRoomRoom, _room_item_id):
                _room_item_obj = get_game_item(_room_item_id, TavernMyRoomRoom)
                if _room_item_obj is not None:
                    current_action_items.append(MenuItem(str(runtime_item_display_name(_room_item_id) or _room_item_id), Call("TavernMyRoomObjectMenu", _room_item_id)))
    $ current_action_items.extend(list(room_menu["actions"]))
    return


label TavernMyRoomObjectMenu(object_id="", refresh_only=False):
    if str(object_id or "") != "":
        $ current_object_id = str(object_id or "")
    $ object_id = str(current_object_id or "")
    $ _room_object = tavern_my_room_get_object(object_id)
    if _room_object is None:
        call TavernMyRoomBuildActions
        return

    if str(action_override_text or "") != "":
        $ MainTxt = str(action_override_text or "")
        $ CurLocDesc = MainTxt
        $ action_override_text = ""
    else:
        $ MainTxt = str(_room_object.description or "")
        $ CurLocDesc = MainTxt
    python:
        _object_picture = str(getattr(_room_object, "picture", "") or "").strip()
        if _object_picture and renpy.loadable(_object_picture):
            scene_image = _object_picture
            _layout_last_picture = _object_picture
        else:
            _default_picture = tavern_my_room_dynamic_picture()
            scene_image = _default_picture or None
            if _default_picture:
                _layout_last_picture = _default_picture
    $ current_action_title = str(_room_object.name or "Действия")
    $ current_action_content = None
    $ current_action_items = []
    python:
        _room_floor_item = _room_has_item_by_id(TavernMyRoomRoom, object_id)
        _takeable_floor_item = _room_floor_item and object_id in ("recipe_book_001", "rusty_hunter_rifle_001", "old_leather_cuirass_001")
        for _room_action in _room_object.visible_actions():
            _room_args = tuple(getattr(_room_action, "args", ()) or ())
            if _room_action.hook == "text":
                current_action_items.append(MenuItem(_room_action.label, Call("TavernMyRoomObjectText", object_id, _room_action.action_id)))
            elif not _takeable_floor_item and _room_action.hook == "call" and str(_room_action.target or "") != "":
                current_action_items.append(MenuItem(_room_action.label, Call(_room_action.target, *_room_args)))
            elif not _takeable_floor_item and _room_action.hook == "jump" and str(_room_action.target or "") != "":
                current_action_items.append(MenuItem(_room_action.label, Jump(_room_action.target)))
        if _takeable_floor_item:
            if object_id == "recipe_book_001":
                current_action_items.append(MenuItem("Сесть за стол", Call("TavernMyRoomTableMenu")))
            current_action_items.append(MenuItem("Взять", Call("TavernMyRoomTakeFloorItem", object_id)))
        current_action_items.append(MenuItem("Назад", Call("TavernMyRoomRestore")))
    if not refresh_only:
        $ renpy.pause(hard=True)
    return


label TavernMyRoomObjectText(object_id="", action_id=""):
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
            MainTxt = _room_text
            CurLocDesc = _room_text
            current_action_title = _room_name or "Действия"
            action_override_text = _room_text
    call TavernMyRoomObjectMenu(object_id)
    return


label TavernMyRoomRestore:
    $ _my_room_picture, _my_room_text = tavern_my_room_scene_state()
    $ scene_image = _my_room_picture or None
    if _my_room_picture:
        $ _layout_last_picture = _my_room_picture
    $ MainTxt = _my_room_text
    $ CurLocDesc = _my_room_text
    call TavernMyRoomBuildActions
    return


label TavernMyRoomTakeFloorItem(item_id=""):
    $ _item_id = str(item_id or "").strip()
    $ _take_result = take(TavernMyRoomRoom, _item_id)
    call TavernMyRoomBuildActions
    $ MainTxt = str((_take_result or {}).get("text", "") or "Вы забираете вещь.")
    $ CurLocDesc = MainTxt
    show screen main_ui
    $ renpy.restart_interaction()
    $ renpy.pause(hard=True)
    return


label TavernMyRoomOpenChest:
    $ _room_object = tavern_my_room_get_object("chest_001")
    if _room_object is not None:
        $ _room_object.state["open"] = 1
    $ MainTxt = "Вы открываете ларь. Внутри хранится ваша одежда."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Ларь"
    $ current_action_content = None
    $ current_action_items = []
    python:
        _all_dresses = [str(_dress or "") for _dress in list(MyDresses or []) if str(_dress or "").strip()]
        _current_dress = str(MyCurDress or "").strip()
        _available_dresses = [d for d in _all_dresses if d != _current_dress]
        if len(_available_dresses) <= 0:
            MainTxt = "В ларе пока пусто."
            CurLocDesc = MainTxt
        else:
            for _dress in _available_dresses:
                _short = str(ShortDressName.get(_dress, _dress)).lower()
                current_action_items.append(MenuItem("Надеть " + _short, Call("TavernMyRoomWearDress", _dress)))
                if player_can_tear_wardrobe_dress(_dress):
                    current_action_items.append(MenuItem("Порвать " + _short + " на лоскуты", Call("TavernMyRoomTearDressToCloth", _dress)))
    $ current_action_items.append(MenuItem("Закрыть ларь", Call("TavernMyRoomCloseChest")))
    show screen main_ui
    $ renpy.pause(hard=True)
    return


label TavernMyRoomCloseChest:
    $ _room_object = tavern_my_room_get_object("chest_001")
    if _room_object is not None:
        $ _room_object.state["open"] = 0
    call TavernMyRoomRestore
    show screen main_ui
    $ renpy.pause(hard=True)
    return


label TavernMyRoomSleepAction:
    call Sleep("TavernMyRoom", 1, "Вы ложитесь на кровать и быстро проваливаетесь в сон.", "TavernMyRoom", "bed_001")


label TavernMyRoomTableMenu:
    if not tavern_my_room_has_recipe_book_access():
        $ _default_picture = tavern_my_room_dynamic_picture()
        $ scene_image = _default_picture or None
        if _default_picture:
            $ _layout_last_picture = _default_picture
        $ MainTxt = "Вам сейчас нечем здесь заняться."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Стол"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Назад", Call("TavernMyRoomRestore"))]
    else:
        $ _table_picture = tavern_my_room_table_picture()
        $ scene_image = _table_picture or None
        if _table_picture:
            $ _layout_last_picture = _table_picture
        if tavern_my_room_has_floor_item("recipe_book_001"):
            $ MainTxt = "На столе уже лежит старая книга с рецептами. Здесь можно спокойно читать записи и сразу пробовать что-нибудь мастерить."
        else:
            $ MainTxt = "Вы раскладываете на столе книгу с рецептами, ингредиенты и всякую мелочь для нехитрой работы руками. Отсюда удобно и читать записи, и сразу что-нибудь мастерить."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Стол"
        $ current_action_content = None
        $ current_action_items = []
        $ current_action_items.append(MenuItem("Читать книгу рецептов", Call("TavernMyRoomTableRead")))
        $ current_action_items.append(MenuItem("Создать предмет", Call("TavernMyRoomTableCraftMenu")))
        $ current_action_items.append(MenuItem("Назад", Call("TavernMyRoomRestore")))
    show screen main_ui
    $ renpy.restart_interaction()
    $ renpy.pause(hard=True)
    return



label TavernMyRoomTableRead(recipe_id=""):
    if not tavern_my_room_has_recipe_book_access():
        call TavernMyRoomTableMenu
        return
    $ _table_recipe_id = str(recipe_id or recipe_book_resolved_selected_id() or "").strip()
    $ _table_picture = recipe_page_image_path(_table_recipe_id) or tavern_my_room_table_picture()
    $ scene_image = _table_picture or None
    if _table_picture:
        $ _layout_last_picture = _table_picture
    if len(list(visible_recipe_pages() or [])) <= 0:
        $ MainTxt = "Вы раскрываете записи на столе, но пока не можете разобрать ни одного полезного рецепта."
        $ CurLocDesc = MainTxt
        $ current_action_title = "Рецепты"
        $ current_action_content = None
        $ current_action_items = [MenuItem("Назад к столу", Call("TavernMyRoomTableMenu"))]
        return
    $ MainTxt = recipe_book_page_text(_table_recipe_id)
    $ CurLocDesc = MainTxt
    $ current_action_title = recipe_book_selected_title(_table_recipe_id)
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _recipe_id in list(visible_recipe_pages() or []):
            _page = get_recipe_page(_recipe_id)
            if _page is None:
                continue
            _title = str(getattr(_page, "title", _recipe_id) or _recipe_id)
            if str(_recipe_id or "") == str(_table_recipe_id or ""):
                _title += " (открыто)"
            current_action_items.append(MenuItem(_title, Call("TavernMyRoomTableRead", _recipe_id)))
    $ current_action_items.append(MenuItem("Назад к столу", Call("TavernMyRoomTableMenu")))
    return


label TavernMyRoomTableCraftMenu:
    if not tavern_my_room_has_recipe_book_access():
        call TavernMyRoomTableMenu
        return
    $ _table_picture = tavern_my_room_table_picture()
    $ scene_image = _table_picture or None
    if _table_picture:
        $ _layout_last_picture = _table_picture
    $ MainTxt = "Вы раскладываете на столе все, что может пригодиться для работы, и прикидываете, что можно сделать прямо сейчас."
    $ CurLocDesc = MainTxt
    $ current_action_title = "Верстак"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _recipe_id in list(visible_recipe_pages() or []):
            if not recipe_page_can_craft(_recipe_id):
                continue
            _page = get_recipe_page(_recipe_id)
            _result_item = get_game_item(str(getattr(_page, "item_result", "") or "").strip()) if _page is not None else None
            _result_name = str(getattr(_result_item, "name", getattr(_page, "item_result", "предмет")) or getattr(_page, "item_result", "предмет"))
            current_action_items.append(MenuItem("Сделать: " + _result_name, Call("TavernMyRoomTableCraftItem", _recipe_id)))
    if len(list(current_action_items or [])) <= 0:
        $ MainTxt = MainTxt + "\n\nСейчас для ваших рецептов не хватает нужных вещей."
        $ CurLocDesc = MainTxt
    $ current_action_items.append(MenuItem("Назад к столу", Call("TavernMyRoomTableMenu")))
    return


label TavernMyRoomTableCraftItem(recipe_id=""):
    $ _table_recipe_id = str(recipe_id or "").strip()
    $ _craft_result = apply_recipe_craft(_table_recipe_id)
    if str(_table_recipe_id or "") == "soap_recipe" and backyard_has_ash_barrel():
        $ _craft_picture = "images/tavern/backyard/soap_backyard.png"
    else:
        $ _craft_picture = tavern_my_room_table_picture()
    $ scene_image = _craft_picture or None
    if _craft_picture:
        $ _layout_last_picture = _craft_picture
    if bool(_craft_result.get("ok", False)):
        $ MainTxt = str(_craft_result.get("text", "") or "Вы мастерите новую вещь по рецепту.")
    else:
        $ MainTxt = str(_craft_result.get("text", "") or "Сейчас для этого дела не хватает нужных вещей.")
    $ CurLocDesc = MainTxt
    $ current_action_title = "Верстак"
    $ current_action_content = None
    $ current_action_items = [
        MenuItem("Продолжить работу", Call("TavernMyRoomTableCraftMenu")),
        MenuItem("Читать записи", Call("TavernMyRoomTableRead", _table_recipe_id)),
        MenuItem("Назад к столу", Call("TavernMyRoomTableMenu")),
    ]
    return


label TavernMyRoomWearDress(dress_code=""):
    $ _dress = str(dress_code or "")
    if _dress != "":
        $ MyCurDress = _dress
        if not isinstance(PlayerDressDaySt, dict):
            $ PlayerDressDaySt = {}
        if _dress not in PlayerDressDaySt:
            $ PlayerDressDaySt[_dress] = int(dayspassed or 0)
        call stat
        $ _short = str(ShortDressName.get(_dress, _dress) or _dress).lower()
        $ _desc = str(FullDressDesc.get(_dress, DressDesc.get(_dress, "")) or "").strip()
        if _desc:
            $ MainTxt = "Вы надели [_short]. " + _desc
        else:
            $ MainTxt = "Вы надели [_short]."
        $ CurLocDesc = MainTxt
    call TavernMyRoomOpenChest
    return


label TavernMyRoomTearDressToCloth(dress_code=""):
    $ _tear_result = player_tear_wardrobe_dress(dress_code)
    $ MainTxt = str((_tear_result or {}).get("text", "") or "Вы откладываете одежду в сторону.")
    $ CurLocDesc = MainTxt
    call TavernMyRoomOpenChest
    return
