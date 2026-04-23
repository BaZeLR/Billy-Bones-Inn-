define recipe_names = []
define recipe_pages = {}
default RecipeBookSelectedId = ""
default RecipeBookReturnRoomCode = ""
default RecipeBookReturnObjectId = ""
default RecipeBookReturnPicture = ""

init 4 python:
    class RecipePage(object):
        def __init__(self, recipe_id, title, image, item_result=None, ingredients=None, unlocked=False, unlock_condition=None, result_quantity=1, notes=None, craft_handler=None):
            self.recipe_id = str(recipe_id or "").strip()
            self.title = str(title or "").strip()
            self.image = str(image or "").strip()
            self.item_result = str(item_result or "").strip()
            self.ingredients = dict(ingredients or {})
            self.unlocked = bool(unlocked)
            self.unlock_condition = unlock_condition
            self.result_quantity = max(1, int(result_quantity or 1))
            self.notes = list(notes or [])
            self.craft_handler = craft_handler

    def register_recipe_page(page_obj):
        if page_obj is None:
            return
        recipe_id = str(getattr(page_obj, "recipe_id", "") or "").strip()
        if not recipe_id:
            return
        recipe_pages[recipe_id] = page_obj
        if recipe_id not in recipe_names:
            recipe_names.append(recipe_id)

    def get_recipe_page(recipe_id):
        return recipe_pages.get(str(recipe_id or "").strip(), None)

    def recipe_page_image_path(recipe_id):
        page = get_recipe_page(recipe_id)
        if page is None:
            return ""
        image_path = str(getattr(page, "image", "") or "").strip()
        if image_path and renpy.loadable(image_path):
            return image_path
        return ""

    def recipe_page_is_unlocked(recipe_id):
        page = get_recipe_page(recipe_id)
        if page is None:
            return False
        if bool(getattr(page, "unlocked", False)):
            return True
        unlock_condition = getattr(page, "unlock_condition", None)
        if callable(unlock_condition):
            try:
                return bool(unlock_condition())
            except Exception:
                return False
        return False

    def visible_recipe_pages():
        return [recipe_id for recipe_id in list(recipe_names or []) if recipe_page_is_unlocked(recipe_id)]

    def recipe_page_ingredient_item_ids(recipe_id):
        page = get_recipe_page(recipe_id)
        if page is None:
            return []
        ingredient_ids = []
        for raw_key, raw_spec in dict(getattr(page, "ingredients", {}) or {}).items():
            spec = dict(raw_spec or {})
            if bool(spec.get("special", "")):
                continue
            alternatives = list(spec.get("alternatives", []) or [])
            if len(alternatives) <= 0:
                alternatives = [str(raw_key or "").strip()]
            for item_id in alternatives:
                item_key = str(item_id or "").strip()
                if item_key and item_key not in ingredient_ids:
                    ingredient_ids.append(item_key)
        return ingredient_ids

    def recipe_ingredient_display_name(item_id):
        item_obj = get_game_item(item_id)
        if item_obj is None:
            return str(item_id or "").strip()
        return str(getattr(item_obj, "name", item_id) or item_id)

    def recipe_ingredient_spawn_hint(item_id):
        item_obj = get_game_item(item_id)
        if item_obj is None:
            return ""
        custom_props = dict(getattr(item_obj, "custom_properties", {}) or {})
        zones = list(custom_props.get("spawn_zones", []) or [])
        rarity = str(custom_props.get("spawn_rarity", "") or "").strip()
        if len(zones) <= 0 and rarity == "":
            return ""
        zone_text = ", ".join([str(zone or "") for zone in zones if str(zone or "").strip() != ""])
        if zone_text and rarity:
            return "Где искать: {}. Редкость: {}.".format(zone_text, rarity)
        if zone_text:
            return "Где искать: {}.".format(zone_text)
        return "Редкость: {}.".format(rarity)

    def recipe_page_requirement_status(recipe_id):
        page = get_recipe_page(recipe_id)
        if page is None:
            return []
        rows = []
        for raw_key, raw_spec in dict(getattr(page, "ingredients", {}) or {}).items():
            spec = dict(raw_spec or {})
            qty = max(1, int(spec.get("quantity", 1) or 1))
            unit = str(spec.get("unit", "") or "").strip()
            note = str(spec.get("note", "") or "").strip()
            special_key = str(spec.get("special", "") or "").strip()
            alternatives = [str(v or "").strip() for v in list(spec.get("alternatives", []) or []) if str(v or "").strip() != ""]
            if len(alternatives) <= 0 and not special_key:
                alternatives = [str(raw_key or "").strip()]

            if special_key == "soap_ash_barrel_ready":
                present = soap_ash_barrel_is_ready()
                display_name = "зольная бочка для щелока"
            elif special_key == "soap_container":
                present = player_has_soap_bowl()
                display_name = "ведро или ночная миска"
            else:
                present = False
                display_name = " / ".join([recipe_ingredient_display_name(v) for v in alternatives])
                for item_id in alternatives:
                    if _player_item_count_by_id(item_id) >= qty:
                        present = True
                        break

            rows.append({
                "name": display_name,
                "quantity": qty,
                "unit": unit,
                "present": present,
                "note": note,
                "hint": "" if special_key else " ".join([recipe_ingredient_spawn_hint(v) for v in alternatives if recipe_ingredient_spawn_hint(v) != ""]).strip(),
            })
        return rows

    def recipe_page_can_craft(recipe_id):
        page = get_recipe_page(recipe_id)
        if page is None or not recipe_page_is_unlocked(recipe_id):
            return False
        for row in recipe_page_requirement_status(recipe_id):
            if not bool(row.get("present", False)):
                return False
        return True

    def recipe_page_text(recipe_id):
        page = get_recipe_page(recipe_id)
        if page is None:
            return "Ничего разборчивого на этой странице не осталось."
        lines = []
        lines.append("Рецепт: {}.".format(str(getattr(page, "title", recipe_id) or recipe_id)))
        result_item = get_game_item(getattr(page, "item_result", ""))
        if result_item is not None:
            lines.append("Результат: {} x{}.".format(str(getattr(result_item, "name", page.item_result) or page.item_result), int(getattr(page, "result_quantity", 1) or 1)))
        elif str(getattr(page, "item_result", "") or "").strip() != "":
            lines.append("Результат: {} x{}.".format(str(page.item_result), int(getattr(page, "result_quantity", 1) or 1)))
        lines.append("")
        lines.append("Нужно:")
        for row in recipe_page_requirement_status(recipe_id):
            status = "есть" if bool(row.get("present", False)) else "нет"
            unit_text = " " + str(row.get("unit", "") or "").strip() if str(row.get("unit", "") or "").strip() else ""
            lines.append("- {} x{}{} ({}).".format(str(row.get("name", "") or ""), int(row.get("quantity", 1) or 1), unit_text, status))
            if str(row.get("note", "") or "").strip() != "":
                lines.append("  " + str(row.get("note", "") or "").strip())
            if str(row.get("hint", "") or "").strip() != "":
                lines.append("  " + str(row.get("hint", "") or "").strip())
        for note_line in list(getattr(page, "notes", []) or []):
            if str(note_line or "").strip() != "":
                lines.append("")
                lines.append(str(note_line or "").strip())
        return "\n".join(lines)

    def recipe_page_missing_lines(recipe_id):
        rows = []
        for row in recipe_page_requirement_status(recipe_id):
            if bool(row.get("present", False)):
                continue
            line = "- Не хватает: {} x{}".format(str(row.get("name", "") or ""), int(row.get("quantity", 1) or 1))
            unit_text = str(row.get("unit", "") or "").strip()
            if unit_text:
                line += " " + unit_text
            rows.append(line + ".")
        return rows

    def recipe_book_resolved_selected_id():
        selected_id = str(RecipeBookSelectedId or "").strip()
        if selected_id and recipe_page_is_unlocked(selected_id):
            return selected_id
        visible_ids = list(visible_recipe_pages() or [])
        if len(visible_ids) > 0:
            return str(visible_ids[0] or "").strip()
        return ""

    def recipe_book_selected_title(recipe_id):
        page = get_recipe_page(recipe_id)
        if page is None:
            return "Рецепты"
        return "Рецепт: " + str(getattr(page, "title", recipe_id) or recipe_id)

    def recipe_book_read_text():
        visible_ids = list(visible_recipe_pages() or [])
        if len(visible_ids) <= 0:
            return "Вы листаете старую книгу, но пока не можете разобрать ни одного полезного рецепта."
        extra_line = ""
        try:
            if int(effective_player_exploration() or 0) < 100:
                extra_line = "\n\nМежду читаемыми страницами заметно, что в книге есть и другие записи, но чернила выцвели, а рука автора слишком неровная. Пока вы разбираете лишь самые понятные рецепты."
        except Exception:
            extra_line = ""
        return "Вы осторожно перелистываете очень старую книгу с рецептами.\n\n" + str(recipe_page_text(recipe_book_resolved_selected_id()) or "") + str(extra_line or "")

    def recipe_book_page_text(recipe_id):
        resolved_id = str(recipe_id or recipe_book_resolved_selected_id() or "").strip()
        if not resolved_id:
            return "Вы листаете старую книгу, но пока не можете разобрать ни одного полезного рецепта."
        page = get_recipe_page(resolved_id)
        if page is None:
            return "Страница выцвела настолько, что разобрать рецепт уже нельзя."

        lines = []
        lines.append("Вы осторожно раскрываете старую книгу на нужной странице.")
        lines.append("")
        lines.append(str(recipe_page_text(resolved_id) or ""))

        missing_lines = list(recipe_page_missing_lines(resolved_id) or [])
        if len(missing_lines) > 0:
            lines.append("")
            lines.append("Сейчас для этого рецепта у вас не хватает следующего:")
            lines.extend(missing_lines)
        else:
            result_item = get_game_item(str(getattr(page, "item_result", "") or "").strip())
            result_name = str(getattr(result_item, "name", getattr(page, "item_result", "")) or getattr(page, "item_result", "предмет"))
            result_qty = int(getattr(page, "result_quantity", 1) or 1)
            lines.append("")
            lines.append("Все нужное у вас при себе. Можно сразу приготовить: {} x{}.".format(result_name, result_qty))

        return "\n".join(lines)

    def recipe_book_apply_picture(recipe_id):
        picture_path = str(recipe_page_image_path(recipe_id) or "").strip()
        globals()["scene_image"] = picture_path
        globals()["_layout_last_picture"] = picture_path

    def recipe_book_restore_picture():
        restore_picture = str(RecipeBookReturnPicture or "").strip()
        globals()["scene_image"] = restore_picture
        globals()["_layout_last_picture"] = restore_picture

    def recipe_book_build_actions(selected_id, where_id="", object_id=""):
        resolved_id = str(selected_id or recipe_book_resolved_selected_id() or "").strip()
        globals()["current_action_title"] = recipe_book_selected_title(resolved_id) if resolved_id else "Рецепты"
        globals()["current_action_content"] = None
        globals()["current_action_items"] = []

        for recipe_id in list(visible_recipe_pages() or []):
            page = get_recipe_page(recipe_id)
            if page is None:
                continue
            title = str(getattr(page, "title", recipe_id) or recipe_id)
            if str(recipe_id or "") == resolved_id:
                title += " (открыто)"
            current_action_items.append(MenuItem(title, Call("ReadRecipeBook", "recipe_book_001", where_id, "", object_id or "recipe_book_001", recipe_id)))

        if resolved_id and recipe_page_can_craft(resolved_id):
            page = get_recipe_page(resolved_id)
            result_item = get_game_item(str(getattr(page, "item_result", "") or "").strip()) if page is not None else None
            result_name = str(getattr(result_item, "name", getattr(page, "item_result", "предмет")) or getattr(page, "item_result", "предмет"))
            current_action_items.append(MenuItem("Создать: " + result_name, Call("RecipeBookCraftItem", resolved_id, where_id, object_id or "recipe_book_001")))

        current_action_items.append(MenuItem("Закрыть книгу", Call("RecipeBookClose", where_id, object_id or "recipe_book_001")))

    def apply_recipe_craft(recipe_id):
        page = get_recipe_page(recipe_id)
        if page is None:
            return {"ok": False, "text": "Такого рецепта у вас сейчас нет."}
        if not recipe_page_can_craft(recipe_id):
            return {"ok": False, "text": "Для этого рецепта у вас не хватает нужных ингредиентов или условий."}
        craft_handler = getattr(page, "craft_handler", None)
        if callable(craft_handler):
            return dict(craft_handler() or {})

        for raw_key, raw_spec in dict(getattr(page, "ingredients", {}) or {}).items():
            spec = dict(raw_spec or {})
            qty = max(1, int(spec.get("quantity", 1) or 1))
            consume_flag = bool(spec.get("consume", True))
            if not consume_flag:
                continue
            special_key = str(spec.get("special", "") or "").strip()
            if special_key:
                continue
            alternatives = [str(v or "").strip() for v in list(spec.get("alternatives", []) or []) if str(v or "").strip() != ""]
            if len(alternatives) <= 0:
                alternatives = [str(raw_key or "").strip()]
            for item_id in alternatives:
                if _player_item_count_by_id(item_id) >= qty:
                    _player_remove_item_by_id(item_id, qty)
                    break

        result_item = str(getattr(page, "item_result", "") or "").strip()
        result_qty = max(1, int(getattr(page, "result_quantity", 1) or 1))
        if result_item:
            _player_add_item_by_id(result_item, result_qty)
        return {
            "ok": True,
            "text": "Вы создаете новый предмет по найденному рецепту.",
            "recipe_id": str(recipe_id or ""),
            "item_result": result_item,
            "quantity": result_qty,
        }


label ReadRecipeBook(what_id="", where_id="", fallback_text="", object_id="", recipe_id=""):
    if str(RecipeBookReturnRoomCode or "").strip() == "":
        $ RecipeBookReturnRoomCode = str(where_id or CurLoc or "").strip()
        $ RecipeBookReturnObjectId = str(object_id or what_id or "").strip()
        $ RecipeBookReturnPicture = str(_layout_last_picture or scene_image or "") or ""
    $ RecipeBookSelectedId = str(recipe_id or recipe_book_resolved_selected_id() or "").strip()
    if str(RecipeBookSelectedId or "").strip() == "":
        $ MainTxt = recipe_book_read_text()
        $ CurLocDesc = MainTxt
        call RefreshCurrentActionMenu(where_id, object_id or what_id, True)
        return
    $ recipe_book_apply_picture(RecipeBookSelectedId)
    $ MainTxt = recipe_book_page_text(RecipeBookSelectedId)
    $ CurLocDesc = MainTxt
    $ recipe_book_build_actions(RecipeBookSelectedId, where_id, object_id or what_id)
    return


label RecipeBookCraftItem(recipe_id="", where_id="", object_id=""):
    $ _recipe_id = str(recipe_id or recipe_book_resolved_selected_id() or "").strip()
    if str(_recipe_id or "").strip() == "":
        $ MainTxt = "Вы пока не выбрали рецепт."
        $ CurLocDesc = MainTxt
        call ReadRecipeBook("recipe_book_001", where_id, "", object_id or "recipe_book_001", _recipe_id)
        return
    $ _craft_result = apply_recipe_craft(_recipe_id)
    if bool(_craft_result.get("ok", False)):
        $ MainTxt = str(_craft_result.get("text", "") or "Вы создаете новый предмет по рецепту.") + "\n\n" + str(recipe_book_page_text(_recipe_id) or "")
    else:
        $ MainTxt = str(_craft_result.get("text", "") or "Для этого рецепта у вас не хватает нужных вещей.") + "\n\n" + str(recipe_book_page_text(_recipe_id) or "")
    $ CurLocDesc = MainTxt
    $ recipe_book_apply_picture(_recipe_id)
    $ RecipeBookSelectedId = _recipe_id
    $ recipe_book_build_actions(_recipe_id, where_id, object_id or "recipe_book_001")
    return


label RecipeBookClose(where_id="", object_id=""):
    $ recipe_book_restore_picture()
    $ RecipeBookSelectedId = ""
    $ _return_room_code = str(RecipeBookReturnRoomCode or where_id or CurLoc or "").strip()
    $ _return_object_id = str(RecipeBookReturnObjectId or object_id or "").strip()
    $ RecipeBookReturnRoomCode = ""
    $ RecipeBookReturnObjectId = ""
    $ RecipeBookReturnPicture = ""
    call RefreshCurrentActionMenu(_return_room_code, _return_object_id, True)
    return
