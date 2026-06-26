default saveVersion = 1
define currentVersion = 3

init -100 python:
    def beforeLoadTractirSave():
        ensure_game_item_registry()

    def tractir_save_patch_loaded_state():
        ensure_game_item_registry()
        tractir_save_normalize_rooms()
        tractir_save_remove_owned_unique_items_from_rooms()
        tractir_save_clear_room_ui_cache()

    def tractir_save_normalize_rooms():
        for room_obj in list(roomRegistry.values()):
            if room_obj is None or not hasattr(room_obj, "game_items"):
                continue
            room_obj.game_items = normalize_room_item_rows(getattr(room_obj, "game_items", []))
            room_obj.objects = room_obj.game_items

    def tractir_save_remove_owned_unique_items_from_rooms():
        inventory = _ensure_player_inventory_store()
        owned_unique = set()
        for item_id, raw_count in list(inventory.items()):
            item_key = get_object_id(item_id)
            if not item_key:
                continue
            if int(raw_count or 0) <= 0:
                continue
            item_obj = get_game_item(item_key)
            if item_obj is not None and not bool(getattr(item_obj, "stackable", False)):
                owned_unique.add(item_key)

        equipped_weapon = get_object_id(EquippedWeapon)
        if equipped_weapon:
            owned_unique.add(equipped_weapon)

        if not owned_unique:
            return

        for room_obj in list(roomRegistry.values()):
            if room_obj is None or not hasattr(room_obj, "game_items"):
                continue
            next_rows = [row for row in normalize_room_item_rows(getattr(room_obj, "game_items", [])) if get_object_id(row) not in owned_unique]
            room_obj.game_items = list(next_rows)
            room_obj.objects = room_obj.game_items

    def tractir_save_clear_room_ui_cache():
        global CurrentRoom, current_action_title, current_action_content, current_action_items
        global current_object_id, main_ui_inventory_dropdown_open, main_ui_overlay
        global current_girl_key, UI_selected_char, UI_mode

        UI_mode = "scene"
        current_action_content = None
        current_action_items = []
        current_object_id = ""
        main_ui_inventory_dropdown_open = False
        main_ui_overlay = ""
        current_girl_key = ""
        UI_selected_char = ""

        room_code = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
        if room_code == "":
            return

        room_obj = get_registered_room(room_code)
        if room_obj is not None:
            CurrentRoom = room_obj
            current_action_title = str(getattr(CurrentRoom, "display_name", "") or room_code)

    def updateSave():
        global saveVersion

        try:
            loaded_version = int(saveVersion or 1)
        except (TypeError, ValueError):
            loaded_version = 1

        if loaded_version < 2:
            updateSave_V1()
            loaded_version = 2

        if loaded_version < 3:
            updateSave_V2()
            loaded_version = 3

        tractir_save_patch_loaded_state()
        saveVersion = int(currentVersion or loaded_version)

    def updateSave_V1():
        tractir_save_patch_loaded_state()

    def updateSave_V2():
        tractir_save_patch_loaded_state()


label before_load:
    $ beforeLoadTractirSave()
    return


label after_load:
    $ updateSave()
    $ renpy.block_rollback()
    return
