# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    class RecipeCatalog(object):
        def __init__(self):
            self.pages = {}

        def register(self, page_obj):
            recipe_id = str(getattr(page_obj, "recipe_id", "") or "").strip()
            if recipe_id:
                self.pages[recipe_id] = page_obj
            return page_obj

        def get(self, recipe_id):
            return self.pages.get(str(recipe_id or "").strip(), None)

        def ids(self):
            return list(self.pages.keys())

    recipe_catalog = RecipeCatalog()

    class RecipeBookSession(object):
        def __init__(self):
            self.selected_id = ""

    def recipe_book_item_state():
        item = get_game_item("recipe_book_001")
        return item.state if item is not None else {}

    class RecipePage(object):
        def __init__(self, recipe_id, title, image, item_result=None, ingredients=None, unlocked=False, unlock_condition=None, result_quantity=1, notes=None, craft_minutes=0, craft_text="", craft_failure_text=""):
            self.recipe_id = str(recipe_id or "").strip()
            self.title = str(title or "").strip()
            self.image = str(image or "").strip()
            self.item_result = str(item_result or "").strip()
            self.ingredients = dict(ingredients or {})
            self.unlocked = bool(unlocked)
            self.unlock_condition = unlock_condition
            self.result_quantity = max(1, int(result_quantity or 1))
            self.notes = list(notes or [])
            self.craft_minutes = max(0, int(craft_minutes or 0))
            self.craft_text = str(craft_text or "Вы создаете новый предмет по найденному рецепту.")
            self.craft_failure_text = str(craft_failure_text or "Не удалось взять нужные ингредиенты.")
            recipe_catalog.register(self)

        def craft(self, resolved_rows=None):
            rows = list(resolved_rows if resolved_rows is not None else recipe_page_requirement_status(self.recipe_id))
            consume_result = recipe_consume_required_ingredients(self.recipe_id, rows)
            if not bool(consume_result.get("ok", False)):
                return {"ok": False, "text": str(consume_result.get("text", "") or self.craft_failure_text), "recipe_id": self.recipe_id}
            if self.item_result:
                player.add_item(self.item_result, self.result_quantity)
            if self.craft_minutes > 0:
                calendar_v2.advance_minutes(self.craft_minutes)
            update_stat_state()
            return {"ok": True, "text": self.craft_text, "recipe_id": self.recipe_id, "item_result": self.item_result, "quantity": self.result_quantity}

    def recipe_page_image_path(recipe_id):
        page = recipe_catalog.get(recipe_id)
        if page is None:
            return ""
        image_path = str(getattr(page, "image", "") or "").strip()
        if image_path and renpy.loadable(image_path):
            return image_path
        return ""

    def recipe_page_is_unlocked(recipe_id):
        page = recipe_catalog.get(recipe_id)
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
        return [recipe_id for recipe_id in recipe_catalog.ids() if recipe_page_is_unlocked(recipe_id)]

    def find_unmarked_numbers(count, present_numbers):
        limit = max(0, int(count or 0))
        markers = [idx + 1 for idx in range(limit)]
        for raw_number in list(present_numbers or []):
            number = abs(int(raw_number or 0))
            index = number - 1
            if 0 <= index < limit and markers[index] > 0:
                markers[index] = -markers[index]
        return [idx + 1 for idx in range(limit) if markers[idx] > 0]

    def recipe_book_exploration_value():
        try:
            return int(effective_player_exploration() or 0)
        except Exception:
            return 0

    def recipe_book_hidden_recipes_revealed():
        return bool(recipe_book_item_state().get("hidden_recipes_revealed", False))

    def recipe_book_bat_thread_started():
        try:
            return int(threads["melissaBatProblem"].num or 0) >= 1
        except Exception:
            return False

    def recipe_book_can_notice_hidden_note():
        return (
            player_has_soap_recipe_book()
            and not bool(recipe_book_item_state().get("tiny_note_found", False))
            and recipe_book_bat_thread_started()
            and recipe_book_exploration_value() >= 120
        )

    def recipe_book_secret_status_text():
        if recipe_book_hidden_recipes_revealed():
            return "На нескольких страницах проступили скрытые записи: автор прятал часть рецептов в слабых винных чернилах."
        if bool(recipe_book_item_state().get("tiny_note_found", False)):
            return "Между страницами лежит тонкая вкладка с неровной строкой: \"Сделай строки горячее и прянее; когда скрывать нечего, красота выйдет наружу.\" Похоже, пергамент надо осторожно нагреть и провести по полям вином."
        if recipe_book_can_notice_hidden_note():
            return "Теперь, когда история с летучими тварями под крышей уже началась, ваш дорожный опыт помогает заметить тонкую вкладку между страницами. Ее край почти сливается с пергаментом, но теперь вы точно видите, что это не случайный обрывок."
        if not recipe_book_bat_thread_started():
            return "Между читаемыми страницами заметно, что в книге есть и другие записи, но пока ничто не заставляет вас искать тайный хозяйственный слой так пристально."
        if recipe_book_exploration_value() > 120:
            return "Опыт в дороге помогает вам понимать почерк автора лучше прежнего. В книге явно есть скрытый слой записей, но сначала надо перечитать ее внимательнее."
        if recipe_book_exploration_value() >= 100:
            return "Часть старых записей уже читается легче, хотя некоторые поля все еще выглядят так, будто смысл спрятан под выцветшими чернилами."
        return "Между читаемыми страницами заметно, что в книге есть и другие записи, но чернила выцвели, а рука автора слишком неровная. Пока вы разбираете лишь самые понятные рецепты."

    def recipe_page_ingredient_item_ids(recipe_id):
        page = recipe_catalog.get(recipe_id)
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
                item_key = get_object_id(item_id)
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

    def recipe_ingredient_alternative_rows(alternatives):
        rows = []
        for raw_item_id in list(alternatives or []):
            item_id = get_object_id(raw_item_id)
            if item_id == "":
                continue
            rows.append({
                "item_id": item_id,
                "name": recipe_ingredient_display_name(item_id),
                "owned": max(0, int(player.item_count(item_id) or 0)),
                "hint": recipe_ingredient_spawn_hint(item_id),
            })
        return rows

    def recipe_resolve_ingredient(raw_key, raw_spec):
        spec = dict(raw_spec or {})
        qty = max(1, int(spec.get("quantity", 1) or 1))
        unit = str(spec.get("unit", "") or "").strip()
        note = str(spec.get("note", "") or "").strip()
        special_key = str(spec.get("special", "") or "").strip()
        consume_flag = bool(spec.get("consume", True))
        ingredient_key = str(raw_key or "").strip()

        if special_key == "soap_ash_barrel_ready":
            present = bool(soap_ash_barrel_is_ready())
            return {
                "key": ingredient_key,
                "name": "зольная бочка для щелока",
                "quantity": qty,
                "unit": unit,
                "present": present,
                "note": note,
                "hint": "",
                "special": special_key,
                "consume": False,
                "alternatives": [],
                "matched_item_id": "",
                "matched_name": "",
                "owned_count": 1 if present else 0,
                "missing_count": 0 if present else qty,
            }

        if special_key == "soap_container":
            present = bool(player_has_soap_bowl())
            return {
                "key": ingredient_key,
                "name": "ведро или ночная миска",
                "quantity": qty,
                "unit": unit,
                "present": present,
                "note": note,
                "hint": "",
                "special": special_key,
                "consume": False,
                "alternatives": [],
                "matched_item_id": "",
                "matched_name": "",
                "owned_count": 1 if present else 0,
                "missing_count": 0 if present else qty,
            }

        raw_alternatives = [get_object_id(v) for v in list(spec.get("alternatives", []) or []) if get_object_id(v) != ""]
        if len(raw_alternatives) <= 0:
            item_key = get_object_id(raw_key)
            if item_key:
                raw_alternatives = [item_key]

        alt_rows = recipe_ingredient_alternative_rows(raw_alternatives)
        display_name = " / ".join([str(row.get("name", "") or "") for row in alt_rows])
        if display_name == "":
            display_name = ingredient_key

        matched_item_id = ""
        matched_name = ""
        owned_count = 0
        for row in alt_rows:
            row_owned = max(0, int(row.get("owned", 0) or 0))
            if row_owned > owned_count:
                owned_count = row_owned
            if matched_item_id == "" and row_owned >= qty:
                matched_item_id = str(row.get("item_id", "") or "")
                matched_name = str(row.get("name", "") or "")
                owned_count = row_owned

        present = matched_item_id != ""
        missing_count = 0 if present else max(0, qty - owned_count)
        hints = []
        for row in alt_rows:
            hint = str(row.get("hint", "") or "").strip()
            if hint and hint not in hints:
                hints.append(hint)

        return {
            "key": ingredient_key,
            "name": display_name,
            "quantity": qty,
            "unit": unit,
            "present": present,
            "note": note,
            "hint": " ".join(hints).strip(),
            "special": special_key,
            "consume": consume_flag,
            "alternatives": alt_rows,
            "matched_item_id": matched_item_id,
            "matched_name": matched_name,
            "owned_count": owned_count,
            "missing_count": missing_count,
        }

    def recipe_page_requirement_status(recipe_id):
        page = recipe_catalog.get(recipe_id)
        if page is None:
            return []
        rows = []
        for raw_key, raw_spec in dict(getattr(page, "ingredients", {}) or {}).items():
            rows.append(recipe_resolve_ingredient(raw_key, raw_spec))
        return rows

    def recipe_missing_requirement_indexes(recipe_id, resolved_rows=None):
        rows = list(resolved_rows if resolved_rows is not None else recipe_page_requirement_status(recipe_id))
        present_numbers = []
        for idx, row in enumerate(rows):
            if bool(row.get("present", False)):
                present_numbers.append(idx + 1)
        return [number - 1 for number in find_unmarked_numbers(len(rows), present_numbers)]

    def recipe_missing_requirement_rows(recipe_id, resolved_rows=None):
        rows = list(resolved_rows if resolved_rows is not None else recipe_page_requirement_status(recipe_id))
        return [rows[idx] for idx in recipe_missing_requirement_indexes(recipe_id, rows)]

    def recipe_page_can_craft(recipe_id):
        page = recipe_catalog.get(recipe_id)
        if page is None or not recipe_page_is_unlocked(recipe_id):
            return False
        return len(recipe_missing_requirement_indexes(recipe_id)) <= 0

    def craftable_recipe_pages():
        return [recipe_id for recipe_id in list(visible_recipe_pages() or []) if recipe_page_can_craft(recipe_id)]

    def recipe_result_display_name(recipe_id):
        page = recipe_catalog.get(recipe_id)
        if page is None:
            return "предмет"
        result_item_id = str(getattr(page, "item_result", "") or "").strip()
        result_item = get_game_item(result_item_id)
        return str(getattr(result_item, "name", result_item_id or "предмет") or result_item_id or "предмет")

    def recipe_page_text(recipe_id):
        page = recipe_catalog.get(recipe_id)
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
            unit_text = " " + str(row.get("unit", "") or "").strip() if str(row.get("unit", "") or "").strip() else ""
            if str(row.get("special", "") or "").strip() != "":
                status = "есть" if bool(row.get("present", False)) else "нет"
            else:
                status = "есть {}/{}".format(int(row.get("owned_count", 0) or 0), int(row.get("quantity", 1) or 1)) if bool(row.get("present", False)) else "нет {}/{}".format(int(row.get("owned_count", 0) or 0), int(row.get("quantity", 1) or 1))
                matched_name = str(row.get("matched_name", "") or "").strip()
                if matched_name:
                    status += ", подойдет: " + matched_name
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
        for row in recipe_missing_requirement_rows(recipe_id):
            line = "- Не хватает: {} x{}".format(str(row.get("name", "") or ""), int(row.get("quantity", 1) or 1))
            unit_text = str(row.get("unit", "") or "").strip()
            if unit_text:
                line += " " + unit_text
            if str(row.get("special", "") or "").strip() == "":
                line += " (есть {}/{})".format(int(row.get("owned_count", 0) or 0), int(row.get("quantity", 1) or 1))
            rows.append(line + ".")
        return rows

    def recipe_book_resolved_selected_id():
        selected_id = str(recipe_book.selected_id or "").strip()
        if selected_id and recipe_page_is_unlocked(selected_id):
            return selected_id
        visible_ids = list(visible_recipe_pages() or [])
        if len(visible_ids) > 0:
            return str(visible_ids[0] or "").strip()
        return ""

    def recipe_book_selected_title(recipe_id):
        page = recipe_catalog.get(recipe_id)
        if page is None:
            return "Рецепты"
        return "Рецепт: " + str(getattr(page, "title", recipe_id) or recipe_id)

    def recipe_book_read_text():
        visible_ids = list(visible_recipe_pages() or [])
        if len(visible_ids) <= 0:
            return "Вы листаете старую книгу, но пока не можете разобрать ни одного полезного рецепта."
        extra_line = ""
        status_text = recipe_book_secret_status_text()
        if status_text:
            extra_line = "\n\n" + status_text
        return "Вы осторожно перелистываете очень старую книгу с рецептами.\n\n" + str(recipe_page_text(recipe_book_resolved_selected_id()) or "") + str(extra_line or "")

    def recipe_book_page_text(recipe_id):
        resolved_id = str(recipe_id or recipe_book_resolved_selected_id() or "").strip()
        if not resolved_id:
            return "Вы листаете старую книгу, но пока не можете разобрать ни одного полезного рецепта."
        page = recipe_catalog.get(resolved_id)
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

        status_text = recipe_book_secret_status_text()
        if status_text:
            lines.append("")
            lines.append(status_text)

        return "\n".join(lines)

    def recipe_book_apply_picture(recipe_id):
        return str(recipe_page_image_path(recipe_id) or "").strip()

    def recipe_book_action_state(selected_id, where_id="", object_id=""):
        resolved_id = str(selected_id or recipe_book_resolved_selected_id() or "").strip()
        action_rows = []
        if len(list(craftable_recipe_pages() or [])) > 0:
            action_rows.append(MenuItem("Создать предмет", Call("RecipeBookCraftMenu", where_id, object_id or "recipe_book_001")))

        if recipe_book_can_notice_hidden_note():
            action_rows.append(MenuItem("Достать тонкую вкладку между страницами", Call("RecipeBookFindTinyNote", where_id, object_id or "recipe_book_001", "book")))
        elif bool(recipe_book_item_state().get("tiny_note_found", False)) and not recipe_book_hidden_recipes_revealed():
            action_rows.append(MenuItem("Нагреть пергамент и смазать вином", Call("RecipeBookRevealHiddenRecipes", where_id, object_id or "recipe_book_001", "book")))
        action_rows.append(MenuItem("Закрыть книгу", Call("RecipeBookClose", where_id, object_id or "recipe_book_001")))
        action_rows.append(MenuItem("Назад", Call("RecipeBookList", where_id, object_id or "recipe_book_001")))
        return {
            "title": recipe_book_selected_title(resolved_id) if resolved_id else "Рецепты",
            "items": action_rows,
        }

    def recipe_consume_required_ingredients(recipe_id, resolved_rows=None):
        rows = list(resolved_rows if resolved_rows is not None else recipe_page_requirement_status(recipe_id))
        for row in rows:
            if not bool(row.get("present", False)):
                return {"ok": False, "text": "Для этого рецепта у вас не хватает: {}.".format(str(row.get("name", "ингредиент") or "ингредиент"))}

        consumed = []
        for row in rows:
            if not bool(row.get("consume", True)):
                continue
            if str(row.get("special", "") or "").strip() != "":
                continue
            item_id = str(row.get("matched_item_id", "") or "").strip()
            qty = max(1, int(row.get("quantity", 1) or 1))
            if item_id == "":
                return {"ok": False, "text": "Не удалось выбрать предмет для рецепта: {}.".format(str(row.get("name", "ингредиент") or "ингредиент"))}
            if not player.remove_item(item_id, qty):
                return {"ok": False, "text": "Не удалось взять {} x{} из ваших вещей.".format(recipe_ingredient_display_name(item_id), qty)}
            consumed.append({
                "key": str(row.get("key", "") or ""),
                "item_id": item_id,
                "name": recipe_ingredient_display_name(item_id),
                "quantity": qty,
            })

        return {"ok": True, "consumed": consumed}

    def recipe_consumed_item_id(consumed_rows, ingredient_key, default=""):
        wanted_key = str(ingredient_key or "").strip()
        for row in list(consumed_rows or []):
            if str(row.get("key", "") or "").strip() == wanted_key:
                return str(row.get("item_id", "") or "").strip()
        return str(default or "").strip()

    def recipe_resolved_item_id(resolved_rows, ingredient_key, default=""):
        wanted_key = str(ingredient_key or "").strip()
        for row in list(resolved_rows or []):
            if str(row.get("key", "") or "").strip() == wanted_key:
                return str(row.get("matched_item_id", "") or "").strip() or str(default or "").strip()
        return str(default or "").strip()

    def apply_recipe_craft(recipe_id):
        page = recipe_catalog.get(recipe_id)
        if page is None:
            return {"ok": False, "text": "Такого рецепта у вас сейчас нет."}
        resolved_rows = recipe_page_requirement_status(recipe_id)
        for row in resolved_rows:
            if not bool(row.get("present", False)):
                return {"ok": False, "text": "Для этого рецепта у вас не хватает нужных ингредиентов или условий."}
        if not recipe_page_is_unlocked(recipe_id):
            return {"ok": False, "text": "Для этого рецепта у вас не хватает нужных ингредиентов или условий."}
        return dict(page.craft(resolved_rows) or {})


default recipe_book = RecipeBookSession()


init -5:
    style recipe_book_list_button is button:
        background Solid("#f5ead3d9")
        hover_background Solid("#dfc79ad9")
        padding (14, 8)
        xfill True
        yminimum 48

    style recipe_book_list_button_text is button_text:
        size 19
        color "#1e130c"
        hover_color "#6b3415"


screen recipe_book_page_list(where_id="", object_id="recipe_book_001"):
    zorder 120

    $ _visible_ids = list(visible_recipe_pages() or [])
    $ _split_index = (len(_visible_ids) + 1) // 2
    $ _recipe_columns = (_visible_ids[:_split_index], _visible_ids[_split_index:])
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24

    fixed:
        xpos 12
        ypos 12
        xsize _left_w
        ysize _left_h

        add Transform("images/rpg_message_bg.png", fit="cover")

        vbox:
            xpos 28
            ypos 22
            xsize _left_w - 56
            ysize _left_h - 44
            spacing 12

            text "КНИГА РЕЦЕПТОВ" size 30 color "#1e130c" xalign 0.5
            text "Выберите рецепт, чтобы открыть его страницу." size 18 color "#5a3a24" xalign 0.5

            if _visible_ids:
                hbox:
                    xfill True
                    spacing 16

                    for _column_ids in _recipe_columns:
                        vbox:
                            xsize int((_left_w - 72) / 2)
                            spacing 8

                            for _recipe_id in _column_ids:
                                $ _page = recipe_catalog.get(_recipe_id)
                                if _page is not None:
                                    textbutton str(getattr(_page, "title", _recipe_id) or _recipe_id):
                                        id "recipe_book_list_button_" + _recipe_id
                                        alt "recipe_book_list_button_" + _recipe_id
                                        style "recipe_book_list_button"
                                        text_style "recipe_book_list_button_text"
                                        action [
                                            Hide("recipe_book_page_list"),
                                            Call("ReadRecipeBook", "recipe_book_001", where_id, "", object_id or "recipe_book_001", _recipe_id),
                                        ]
            else:
                text "Пока вы не можете разобрать ни одного полезного рецепта." size 21 color "#2d1d12" xalign 0.5


label RecipeBookList(where_id="", object_id=""):
    hide screen recipe_book_page_list
    $ recipe_book.selected_id = ""
    $ scene_runtime.text = "Вы раскрываете старую книгу. Выберите рецепт, который хотите прочитать."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Книга рецептов"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = [MenuItem("Назад", [Hide("recipe_book_page_list"), Call("RecipeBookClose", where_id, object_id or "recipe_book_001")])]
    show screen recipe_book_page_list(where_id, object_id or "recipe_book_001")
    $ renpy.restart_interaction()
    return


label ReadRecipeBook(what_id="", where_id="", fallback_text="", object_id="", recipe_id=""):
    $ renpy.dynamic("_recipe_picture", "_recipe_action_state")
    hide screen recipe_book_page_list
    if not str(recipe_id or "").strip():
        call RecipeBookList(where_id, object_id or what_id or "recipe_book_001")
        return
    $ recipe_book_item_state()["read_count"] = max(0, int(recipe_book_item_state().get("read_count", 0) or 0)) + 1
    $ recipe_book.selected_id = str(recipe_id or "").strip()
    if not recipe_page_is_unlocked(recipe_book.selected_id):
        call RecipeBookList(where_id, object_id or what_id or "recipe_book_001")
        return
    $ _recipe_picture = recipe_book_apply_picture(recipe_book.selected_id)
    if _recipe_picture:
        $ scene_runtime.picture = _recipe_picture
    $ scene_runtime.text = recipe_book_page_text(recipe_book.selected_id)
    $ scene_runtime.location_text = scene_runtime.text
    $ _recipe_action_state = recipe_book_action_state(recipe_book.selected_id, where_id, object_id or what_id)
    $ main_ui_runtime.action_title = _recipe_action_state["title"]
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = _recipe_action_state["items"]
    return


label RecipeBookFindTinyNote(where_id="", object_id="", return_context="book"):
    $ renpy.dynamic("_recipe_action_state")
    if not recipe_book_can_notice_hidden_note():
        $ scene_runtime.text = "Вы еще раз просматриваете переплет и края страниц, но ничего нового не находите."
    else:
        $ recipe_book_item_state()["tiny_note_found"] = True
        $ recipe_book_item_state()["riddle_seen"] = True
        $ scene_runtime.text = "Вы осторожно вытаскиваете из сгиба тонкую вкладку. Когда я согрета и пьяна, сможешь читать меня,как открытую книгу и видеть все мои тайные места"   
    if str(return_context or "") == "table":
        $ main_ui_runtime.action_title = "Книга рецептов"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = []
        if recipe_book_can_notice_hidden_note():
            $ main_ui_runtime.action_items.append(MenuItem("Достать тонкую вкладку между страницами", Call("RecipeBookFindTinyNote", where_id, object_id or "recipe_book_001", "table")))
        elif bool(recipe_book_item_state().get("tiny_note_found", False)) and not recipe_book_hidden_recipes_revealed():
            $ main_ui_runtime.action_items.append(MenuItem("Нагреть пергамент и смазать вином", Call("RecipeBookRevealHiddenRecipes", where_id, object_id or "recipe_book_001", "table")))
        $ main_ui_runtime.action_items.append(MenuItem("Вернуться к записям", Call("RecipeBookList", where_id, object_id or "recipe_book_001")))
        $ main_ui_runtime.action_items.append(MenuItem("Назад к столу", Call("TavernMyRoomTableMenu")))
    else:
        $ _recipe_action_state = recipe_book_action_state(recipe_book.selected_id, where_id, object_id or "recipe_book_001")
        $ main_ui_runtime.action_title = _recipe_action_state["title"]
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = _recipe_action_state["items"]
    $ renpy.restart_interaction()
    return


label RecipeBookRevealHiddenRecipes(where_id="", object_id="", return_context="book"):
    $ renpy.dynamic("_recipe_picture", "_recipe_action_state")
    if not bool(recipe_book_item_state().get("tiny_note_found", False)):
        $ scene_runtime.text = "Пока вы не понимаете, что именно нужно искать на этих страницах."
    elif recipe_book_hidden_recipes_revealed():
        $ scene_runtime.text = "Скрытые строки уже проявлены. Теперь их можно читать как обычные рецепты."
    elif int(player.tavern_management.winenum or 0) <= 0:
        $ scene_runtime.text = "Для опыта нужен хотя бы глоток вина из запасов трактира. Без него старые поля остаются пустыми."
    else:
        $ recipe_book_item_state()["hidden_recipes_revealed"] = True
        $ recipe_book.selected_id = "bat_repellent_recipe"
        $ scene_runtime.text = "Вы держите пергамент над ровным теплом, пока старые волокна не начинают едва темнеть, потом смачиваете край тряпки вином и осторожно проводите по полям. Через несколько минут под выцветшей желтизной проступают новые строки.\n\nАвтор прятал часть записей намеренно. Среди них есть дымная смесь из сухого мха, лаванды и резких трав - как раз то, чем можно выкурить летучих тварей из-под крыши."
    $ scene_runtime.location_text = scene_runtime.text
    if str(return_context or "") == "table":
        $ main_ui_runtime.action_title = "Книга рецептов"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = []
        if recipe_book_hidden_recipes_revealed():
            $ _recipe_picture = recipe_book_apply_picture(recipe_book.selected_id)
            if _recipe_picture:
                $ scene_runtime.picture = _recipe_picture
            $ main_ui_runtime.action_items.append(MenuItem("Читать проявленный рецепт", Call("ReadRecipeBook", "recipe_book_001", where_id, "", object_id or "recipe_book_001", recipe_book.selected_id)))
            $ main_ui_runtime.action_items.append(MenuItem("Продолжить работу", Call("TavernMyRoomTableCraftMenu")))
        else:
            if recipe_book_can_notice_hidden_note():
                $ main_ui_runtime.action_items.append(MenuItem("Достать тонкую вкладку между страницами", Call("RecipeBookFindTinyNote", where_id, object_id or "recipe_book_001", "table")))
            elif bool(recipe_book_item_state().get("tiny_note_found", False)) and not recipe_book_hidden_recipes_revealed():
                $ main_ui_runtime.action_items.append(MenuItem("Нагреть пергамент и смазать вином", Call("RecipeBookRevealHiddenRecipes", where_id, object_id or "recipe_book_001", "table")))
            $ main_ui_runtime.action_items.append(MenuItem("Вернуться к записям", Call("RecipeBookList", where_id, object_id or "recipe_book_001")))
        $ main_ui_runtime.action_items.append(MenuItem("Назад к столу", Call("TavernMyRoomTableMenu")))
    else:
        $ _recipe_picture = recipe_book_apply_picture(recipe_book.selected_id)
        if _recipe_picture:
            $ scene_runtime.picture = _recipe_picture
        $ _recipe_action_state = recipe_book_action_state(recipe_book.selected_id, where_id, object_id or "recipe_book_001")
        $ main_ui_runtime.action_title = _recipe_action_state["title"]
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = _recipe_action_state["items"]
    $ renpy.restart_interaction()
    return


label RecipeBookCraftMenu(where_id="", object_id=""):
    $ renpy.dynamic("_book_picture", "_craftable_count", "_recipe_id")
    $ _book_picture = recipe_page_image_path(recipe_book.selected_id) or str(scene_runtime.picture or scene_runtime.picture or "")
    if _book_picture:
        $ scene_runtime.picture = _book_picture
    $ scene_runtime.text = "Вы проверяете записи и откладываете в сторону только те рецепты, для которых сейчас есть все нужное."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Создать предмет"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    $ _craftable_count = 0
    python:
        for _recipe_id in list(craftable_recipe_pages() or []):
            _craftable_count += 1
            main_ui_runtime.action_items.append(MenuItem("Сделать: " + recipe_result_display_name(_recipe_id), Call("RecipeBookCraftItem", _recipe_id, where_id, object_id or "recipe_book_001")))
    if int(_craftable_count or 0) <= 0:
        $ scene_runtime.text = "Сейчас ни один рецепт не готов полностью. Прочитайте нужную страницу, чтобы увидеть, чего не хватает."
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_items.append(MenuItem("Закрыть книгу", Call("RecipeBookClose", where_id, object_id or "recipe_book_001")))
    $ main_ui_runtime.action_items.append(MenuItem("Назад", Call("RecipeBookList", where_id, object_id or "recipe_book_001")))
    return


label RecipeBookCraftItem(recipe_id="", where_id="", object_id=""):
    $ renpy.dynamic("_recipe_id", "_craft_result", "_recipe_picture", "_recipe_action_state")
    $ _recipe_id = str(recipe_id or recipe_book_resolved_selected_id() or "").strip()
    if str(_recipe_id or "").strip() == "":
        $ scene_runtime.text = "Вы пока не выбрали рецепт."
        $ scene_runtime.location_text = scene_runtime.text
        call ReadRecipeBook("recipe_book_001", where_id, "", object_id or "recipe_book_001", _recipe_id)
        return
    $ _craft_result = apply_recipe_craft(_recipe_id)
    if bool(_craft_result.get("ok", False)):
        $ scene_runtime.text = str(_craft_result.get("text", "") or "Вы создаете новый предмет по рецепту.") + "\n\n" + str(recipe_book_page_text(_recipe_id) or "")
    else:
        $ scene_runtime.text = str(_craft_result.get("text", "") or "Для этого рецепта у вас не хватает нужных вещей.") + "\n\n" + str(recipe_book_page_text(_recipe_id) or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ _recipe_picture = recipe_book_apply_picture(_recipe_id)
    if _recipe_picture:
        $ scene_runtime.picture = _recipe_picture
    $ recipe_book.selected_id = _recipe_id
    $ _recipe_action_state = recipe_book_action_state(_recipe_id, where_id, object_id or "recipe_book_001")
    $ main_ui_runtime.action_title = _recipe_action_state["title"]
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = _recipe_action_state["items"]
    return


label RecipeBookClose(where_id="", object_id=""):
    hide screen recipe_book_page_list
    $ recipe_book.selected_id = ""
    if str(where_id or "") == "TavernMyRoom":
        call TavernMyRoomTableMenu
    else:
        call TavernAticObjectMenu(object_id or "recipe_book_001")
    return
