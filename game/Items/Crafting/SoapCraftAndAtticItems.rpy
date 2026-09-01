# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    class CraftingInfo(object):
        def __init__(self):
            self.ash_barrel_installed = False
            self.ash_barrel_ready_day = 0
            self.pending_soap_batches = []
            self.soap_requests = {}
            self.soap_sample_intro_done = False
            self.soap_sample_given = {}
            self.last_soap_batch_profile = {}
            self.special_cream_recipe_unlocked = False

    SOAP_HOUSEHOLD_IDS = ("sandra", "melissa", "amanda")
    SOAP_PREFERRED_AROMAS = {
        "sandra": "лавандово-травяной",
        "melissa": "лавандово-розовый",
        "amanda": "розово-медовый",
    }

    def attic_room_picture_path():
        picture_path = "images/player_room/player_room_attic.png"
        if renpy.loadable(picture_path):
            return picture_path
        return ""

    def attic_item_picture_path(item_id):
        item_key = str(item_id or "").strip()
        picture_map = {
            "recipe_book_001": "images/recipe_book/recipe_book_attick.png",
            "rusty_hunter_rifle_001": "images/player_room/rifle0.png",
            "old_leather_cuirass_001": attic_room_picture_path(),
        }
        picture_path = str(picture_map.get(item_key, "") or "").strip()
        if picture_path and renpy.loadable(picture_path):
            return picture_path
        item_obj = get_game_item(item_key)
        fallback_picture = str(getattr(item_obj, "picture", "") or "").strip() if item_obj is not None else ""
        if fallback_picture and renpy.loadable(fallback_picture):
            return fallback_picture
        return attic_room_picture_path()

    def attic_manageable_item_ids():
        return tuple(["recipe_book_001", "rusty_hunter_rifle_001", "old_leather_cuirass_001", "cork_001"] + soap_inventory_item_ids())

    def player_has_attic_manageable_items():
        for item_id in attic_manageable_item_ids():
            if player.item_count(item_id) > 0:
                return True
        return False

    def attic_item_equipped_text(item_id):
        item_key = str(item_id or "").strip()
        if item_key == str(player.equipment.weapon or ""):
            return "Сейчас это оружие у вас наготове."
        if item_key == str(player.equipment.armor or ""):
            return "Сейчас эта броня надета на вас."
        return ""

    def rusty_hunter_rifle_item():
        try:
            _direct_item = RustyHunterRifleItem
        except Exception:
            _direct_item = None
        if _direct_item is not None:
            return _direct_item
        return get_game_item("rusty_hunter_rifle_001")

    def rusty_hunter_rifle_is_cleaned():
        rifle_item = rusty_hunter_rifle_item()
        if rifle_item is None:
            return False
        return int(getattr(rifle_item, "state", {}).get("rust_cleaned", 0) or 0) == 1

    def rusty_hunter_rifle_is_oiled():
        rifle_item = rusty_hunter_rifle_item()
        if rifle_item is None:
            return False
        return int(getattr(rifle_item, "state", {}).get("oiled", 0) or 0) == 1

    def rusty_hunter_rifle_loaded_ammo():
        rifle_item = rusty_hunter_rifle_item()
        return str(getattr(rifle_item, "state", {}).get("loaded_ammo", "") or "").strip() if rifle_item is not None else ""

    def rusty_hunter_rifle_ammo_name(ammo_code=""):
        ammo_key = str(ammo_code or "").strip()
        if ammo_key == "arrows":
            return "стрелой"
        if ammo_key == "droplets":
            return "дробью"
        return ""

    def rusty_hunter_rifle_status_lines():
        rows = []
        if rusty_hunter_rifle_is_cleaned():
            rows.append("Ржавчину с механизма уже счистили.")
        else:
            rows.append("Механизм все еще покрыт ржавчиной.")
        if rusty_hunter_rifle_is_oiled():
            rows.append("Ходовые части оружия уже смазаны маслом.")
        else:
            rows.append("Механизм просит хорошей смазки.")
        loaded_ammo = rusty_hunter_rifle_loaded_ammo()
        if loaded_ammo:
            rows.append("Сейчас оружие заряжено {}.".format(rusty_hunter_rifle_ammo_name(loaded_ammo)))
        else:
            rows.append("Сейчас оружие не заряжено.")
        return rows

    def runtime_item_display_name(item_id):
        item_key = str(item_id or "").strip()
        item_obj = get_game_item(item_key)
        item_name = str(getattr(item_obj, "name", "") or item_key).strip() or item_key
        if item_key == "rusty_hunter_rifle_001":
            if rusty_hunter_rifle_is_cleaned() and rusty_hunter_rifle_is_oiled():
                return "охотничья винтовка-арбалет"
            if rusty_hunter_rifle_is_cleaned():
                return "очищенная охотничья винтовка-арбалет"
        return item_name

    def runtime_item_description_text(item_id):
        item_key = str(item_id or "").strip()
        item_obj = get_game_item(item_key)
        if item_obj is None:
            return ""
        if item_key == "rusty_hunter_rifle_001":
            if rusty_hunter_rifle_is_cleaned() and rusty_hunter_rifle_is_oiled():
                return "Старинная охотничья винтовка-арбалет. Вы уже счистили ржавчину и как следует смазали механизм, так что теперь это рабочее оружие, а не ржавый трофей."
            if rusty_hunter_rifle_is_cleaned():
                return "Старинная охотничья винтовка-арбалет. Основную ржавчину вы уже счистили, и оружие выглядит заметно живее, хотя механизму еще не помешает хорошая смазка."
        return str(getattr(item_obj, "description", "") or "").strip()

    def attic_item_menu_caption(item_id):
        caption = runtime_item_display_name(item_id)
        if item_id == str(player.equipment.weapon or ""):
            return caption + " (оружие)"
        if item_id == str(player.equipment.armor or ""):
            return caption + " (надето)"
        return caption

    def _soap_player_has_any(item_ids):
        for item_id in tuple(item_ids or ()):
            if player.item_count(str(item_id or "").strip()) > 0:
                return True
        return False

    def soap_recipe_chain_discovered():
        return player_has_soap_recipe_book() or bool(rooms.get("TavernAtic").state.get("loot_found", False))

    def player_has_soap_recipe_book():
        if player.item_count("recipe_book_001") > 0:
            return True
        try:
            if _room_has_item_by_id(rooms.get("TavernMyRoom"), "recipe_book_001"):
                return True
        except Exception:
            pass
        try:
            if rooms.current is not None and _room_has_item_by_id(rooms.current, "recipe_book_001"):
                return True
        except Exception:
            pass
        return False

    def player_has_soap_bowl():
        return _soap_player_has_any(("night_bowl_001", "bucket_001"))

    def soap_inventory_item_ids(include_luxury=True):
        soap_ids = []
        for item_id, item_obj in dict(game_item_registry or {}).items():
            properties = dict(getattr(item_obj, "custom_properties", {}) or {})
            if str(properties.get("crafted_kind", "") or "").strip() != "soap":
                continue
            if not bool(include_luxury) and str(properties.get("soap_grade", "ordinary") or "ordinary").strip() == "luxury":
                continue
            soap_ids.append(str(item_id))
        return soap_ids

    def soap_available_piece_count():
        return sum(max(0, int(player.item_count(item_id) or 0)) for item_id in soap_inventory_item_ids(False))

    def soap_total_piece_count():
        return sum(max(0, int(player.item_count(item_id) or 0)) for item_id in soap_inventory_item_ids())

    def player_remove_soap_pieces(quantity=1, include_luxury=False):
        remaining = max(0, int(quantity or 0))
        available = soap_total_piece_count() if bool(include_luxury) else soap_available_piece_count()
        if remaining <= 0 or available < remaining:
            return False
        for item_id in soap_inventory_item_ids(include_luxury):
            owned = max(0, int(player.item_count(item_id) or 0))
            take = min(owned, remaining)
            if take > 0:
                player.remove_item(item_id, take)
                remaining -= take
            if remaining <= 0:
                return True
        return False

    def household_soap_preferred_aroma_text(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        return str(SOAP_PREFERRED_AROMAS.get(girl, "душистый") or "душистый")

    def soap_batch_profile(additive_ids=None):
        aroma_ids = []
        for item_id in list(additive_ids or []):
            item_key = str(item_id or "").strip()
            if item_key != "" and item_key not in aroma_ids:
                aroma_ids.append(item_key)

        notes = []
        craft_parts = []
        if "lavender_001" in aroma_ids:
            craft_parts.append("лавандой")
        if "wild_rose_001" in aroma_ids:
            craft_parts.append("дикой розой")
        if "special_herbs_001" in aroma_ids:
            craft_parts.append("редкими душистыми травами")
            notes.append("с терпкой травяной нотой")
        if "honey_comb_001" in aroma_ids:
            craft_parts.append("медовой сладостью")
            notes.append("с медовой сладостью")
        if "olive_oil_001" in aroma_ids:
            notes.append("на более мягкой масляной основе")

        scent_core = "травяной"
        if "lavender_001" in aroma_ids and "wild_rose_001" in aroma_ids:
            scent_core = "лавандово-розовый"
        elif "lavender_001" in aroma_ids:
            scent_core = "лавандовый"
        elif "wild_rose_001" in aroma_ids:
            scent_core = "розовый"
        elif "special_herbs_001" in aroma_ids:
            scent_core = "травяной"

        label = scent_core
        if len(notes) > 0:
            label = label + " " + ", ".join(notes)

        if len(craft_parts) <= 0:
            craft_text = "травами"
        elif len(craft_parts) == 1:
            craft_text = craft_parts[0]
        elif len(craft_parts) == 2:
            craft_text = craft_parts[0] + " и " + craft_parts[1]
        else:
            craft_text = ", ".join(craft_parts[:-1]) + " и " + craft_parts[-1]

        return {
            "aroma_ids": tuple(aroma_ids),
            "label": label,
            "craft_text": craft_text,
        }

    def soap_last_batch_label():
        profile = dict(crafting.last_soap_batch_profile or {})
        return str(profile.get("label", "душистое домашнее") or "душистое домашнее")

    def soap_ash_barrel_is_ready():
        if not crafting.ash_barrel_installed:
            return False
        return current_game_day() >= int(crafting.ash_barrel_ready_day or 0)

    def player_has_rifle_loading_ammo(ammo_code=""):
        ammo_key = str(ammo_code or "").strip()
        if ammo_key == "arrows":
            return player.item_count("arrows_001") > 0
        if ammo_key == "droplets":
            return player.item_count("droplets_001") > 0 and player.item_count("gunpowder_001") > 0
        return False

    def rusty_hunter_rifle_can_clean():
        return player.item_count("rusty_hunter_rifle_001") > 0 and not rusty_hunter_rifle_is_cleaned()

    def rusty_hunter_rifle_can_oil():
        return (
            player.item_count("rusty_hunter_rifle_001") > 0
            and rusty_hunter_rifle_is_cleaned()
            and not rusty_hunter_rifle_is_oiled()
            and player.item_count("weapon_oil_001") > 0
        )

    def rusty_hunter_rifle_can_load(ammo_code=""):
        return (
            player.item_count("rusty_hunter_rifle_001") > 0
            and rusty_hunter_rifle_is_cleaned()
            and rusty_hunter_rifle_is_oiled()
            and rusty_hunter_rifle_loaded_ammo() == ""
            and player_has_rifle_loading_ammo(ammo_code)
        )

    def rusty_hunter_rifle_can_unload():
        return player.item_count("rusty_hunter_rifle_001") > 0 and rusty_hunter_rifle_loaded_ammo() != ""

    def player_can_train_shooting():
        if player.item_count("rusty_hunter_rifle_001") <= 0:
            return False
        if not rusty_hunter_rifle_is_cleaned() or not rusty_hunter_rifle_is_oiled():
            return False
        if rusty_hunter_rifle_loaded_ammo() != "":
            return True
        return player_has_rifle_loading_ammo("arrows") or player_has_rifle_loading_ammo("droplets")

    def shooting_practice_intro_text(room_code=""):
        room_key = str(room_code or rooms.current_code or "").strip()
        if room_key == "Backyard":
            return "Вы присматриваете безопасное место во дворе, ставите у стены старую доску и готовитесь проверить оружие на деле."
        return "Вы выбираете в лесу сухой пень и устраиваете короткую тренировку, чтобы почувствовать оружие в руках."

    def shooting_practice_fire_text(ammo_code="", room_code=""):
        ammo_key = str(ammo_code or "").strip()
        room_key = str(room_code or rooms.current_code or "").strip()
        if ammo_key == "droplets":
            if room_key == "Backyard":
                return "Вы даете короткий выстрел дробью по доске у стены. Грохот прокатывается по двору, а заряд выбивает из дерева облако щепок."
            return "Вы стреляете дробью по сухому пню. Заряд с треском разносит кору, а лес еще немного держит в воздухе эхо выстрела."
        if room_key == "Backyard":
            return "Вы выпускаете стрелу по самодельной мишени во дворе. Стрела уходит ровно, и вы лучше чувствуете, как работает старый механизм."
        return "Вы выпускаете стрелу в лесную мишень. Она с глухим стуком вонзается в древесину, и рука запоминает правильное усилие."

    def soap_can_cook_at_backyard():
        return (
            str(rooms.current_code or "") == "Backyard"
            and soap_ash_barrel_is_ready()
            and player_has_soap_recipe_book()
        )

    CLOTH_DRESS_SCRAP_YIELD = {
        "villagedress": 3,
        "citydress": 5,
        "sailordress": 4,
        "thiefdress": 6,
        "nobbledress": 8,
        "modestworkdress": 4,
        "modestnicedress": 4,
        "workdress": 4,
        "workdresszhilet": 5,
        "greenworkdress": 4,
        "openworkdress": 4,
        "minidress": 4,
        "slutdress": 4,
        "nightshirt": 3,
        "simplebra": 1,
        "simplepanties": 1,
        "whitestockings": 1,
        "blackstockings": 1,
        "redstockings": 1,
    }

    def cloth_scrap_yield_for_dress(dress_code=""):
        code = str(dress_code or "").strip()
        fixed_yield = int(CLOTH_DRESS_SCRAP_YIELD.get(code, 0) or 0)
        if fixed_yield > 0:
            return fixed_yield
        if code in list(MaleDressCodes or []):
            price = int(DressCost.get(code, 0) or 0)
            if price >= 3000:
                return 8
            if price >= 800:
                return 6
            if price >= 250:
                return 5
            return 3
        if code in list(FemaleDressCodes or []):
            price = int(DressCost.get(code, 0) or 0)
            if price >= 450:
                return 5
            if price >= 150:
                return 4
            return 1
        return 0

    def player_can_tear_wardrobe_dress(dress_code="", allow_worn=False):
        dress_name = str(dress_code or "").strip()
        if dress_name == "":
            return False
        appearance = player.appearance
        if not bool(allow_worn) and dress_name == str(appearance.current_dress or "").strip():
            return False
        if cloth_scrap_yield_for_dress(dress_name) <= 0:
            return False
        return appearance.has_dress(dress_name)

    def player_tear_wardrobe_dress(dress_code="", allow_worn=False, context_text=""):
        appearance = player.appearance
        dress_name = str(dress_code or "").strip()
        worn_now = dress_name == str(appearance.current_dress or "").strip()
        if worn_now and not bool(allow_worn):
            return {"ok": False, "text": "Сначала снимите одежду. Рвать можно только то, что уже лежит в ларе."}
        if not player_can_tear_wardrobe_dress(dress_name, allow_worn):
            return {"ok": False, "text": "Эту одежду сейчас нельзя пустить на лоскуты."}
        scrap_qty = cloth_scrap_yield_for_dress(dress_name)
        appearance.destroy_dress(dress_name)
        player.add_item("cloth_scrap_001", scrap_qty)
        try:
            update_stat_state()
        except Exception:
            pass
        dress_name_short = str(ShortDressName.get(dress_name, dress_name) or dress_name).lower()
        if str(context_text or "").strip():
            result_text = str(context_text or "").strip()
        elif worn_now:
            result_text = "Ткань не выдерживает и рвется прямо на вас. От одежды остаются только лоскуты x{}.".format(scrap_qty)
        else:
            result_text = "Вы рвете {} на полосы ткани и убираете их в свои вещи. Теперь у вас есть лоскуты x{}.".format(dress_name_short, scrap_qty)
        return {
            "ok": True,
            "quantity": scrap_qty,
            "worn": bool(worn_now),
            "text": result_text,
        }

    def player_tear_worn_dress_context(context_text=""):
        current_dress = str(player.appearance.current_dress or "").strip()
        if current_dress == "":
            return {"ok": False, "text": "На вас уже нечему рваться."}
        return player_tear_wardrobe_dress(current_dress, True, context_text)

    def soap_recipe_ingredients(*additive_ids):
        ingredients = {
            "soap_container": {
                "quantity": 1,
                "unit": "штука",
                "special": "soap_container",
                "consume": False,
                "note": "Подойдет ведро или ночная миска.",
            },
            "ash_barrel_ready": {
                "quantity": 1,
                "unit": "штука",
                "special": "soap_ash_barrel_ready",
                "consume": False,
                "note": "Нужен щелок из зольной бочки, простоявший не меньше недели.",
            },
            "pig_lard_001": {"quantity": 1, "unit": "кусок"},
        }
        for item_id in tuple(additive_ids or ()):
            ingredients[str(item_id)] = {"quantity": 1, "unit": "порция"}
        return ingredients

    class SoapBatchRecipePage(RecipePage):
        def craft(self, resolved_rows=None):
            rows = list(resolved_rows if resolved_rows is not None else recipe_page_requirement_status(self.recipe_id))
            consume_result = recipe_consume_required_ingredients(self.recipe_id, rows)
            if not bool(consume_result.get("ok", False)):
                return {"ok": False, "text": str(consume_result.get("text", "") or self.craft_failure_text), "recipe_id": self.recipe_id}
            soap_additives = [
                str(row.get("item_id", "") or "")
                for row in list(consume_result.get("consumed", []) or [])
                if str(row.get("item_id", "") or "") in ("lavender_001", "wild_rose_001", "special_herbs_001", "honey_comb_001", "olive_oil_001")
            ]
            batch_profile = soap_batch_profile(soap_additives)
            player.change_stat("fun", 20)
            calendar_v2.advance_minutes(self.craft_minutes)
            crafting.last_soap_batch_profile = dict(batch_profile)
            crafting.pending_soap_batches.append({"item_id": self.item_result, "quantity": self.result_quantity, "ready_day": current_game_day() + 7, "profile": dict(batch_profile)})
            crafting.ash_barrel_ready_day = current_game_day() + 7
            update_stat_state()
            result_item = get_game_item(self.item_result)
            result_name = str(getattr(result_item, "name", self.item_result) or self.item_result)
            return {"ok": True, "text": "Вы разводите огонь во дворе, берете настоявшийся щелок из зольной бочки, кипятите его с {} и затем раскладываете густую массу по формам. Получится {}; запах у партии выходит {}. Теперь мылу нужно как следует вылежаться: партия будет готова примерно через {{b}}неделю{{/b}}.".format(batch_profile.get("craft_text", "травами"), result_name, batch_profile.get("label", "травяной")), "recipe_id": self.recipe_id, "item_result": self.item_result, "quantity": self.result_quantity}

    class LibidoTinctureRecipePage(RecipePage):
        def craft(self, resolved_rows=None):
            rows = list(resolved_rows if resolved_rows is not None else recipe_page_requirement_status(self.recipe_id))
            consume_result = recipe_consume_required_ingredients(self.recipe_id, rows)
            if not bool(consume_result.get("ok", False)):
                return {"ok": False, "text": str(consume_result.get("text", "") or self.craft_failure_text), "recipe_id": self.recipe_id}
            flavor_item = recipe_consumed_item_id(consume_result.get("consumed", []), "flavor_mix", "")
            if self.item_result:
                player.add_item(self.item_result, self.result_quantity)
            calendar_v2.advance_minutes(self.craft_minutes)
            update_stat_state()
            flavor_name = "терпкие травы" if flavor_item == "special_herbs_001" else "раздавленные ягоды"
            return {"ok": True, "text": self.craft_text.format(flavor_name), "recipe_id": self.recipe_id, "item_result": self.item_result, "quantity": self.result_quantity}

    def libido_recipe_selected_flavor_item():
        if player.item_count("special_herbs_001") > 0:
            return "special_herbs_001"
        if player.item_count("berries_001") > 0:
            return "berries_001"
        return ""

    """
    Retired callback implementations were replaced by RecipePage.craft and the two
    recipe subclasses above. Keeping the old bodies would create a second crafting
    authority, so standard consume/produce/time behavior now lives on each page.
    """

    def player_can_use_soap(item_id=""):
        item_key = str(item_id or "").strip()
        return item_key in soap_inventory_item_ids() and player.item_count(item_key) > 0

    def crafting_release_ready_soap_batches():
        current_day = current_game_day()
        remaining_pending = []
        released = 0
        for batch in list(crafting.pending_soap_batches or []):
            batch_data = dict(batch or {})
            quantity = max(0, int(batch_data.get("quantity", 0) or 0))
            ready_day = int(batch_data.get("ready_day", 0) or 0)
            profile = dict(batch_data.get("profile", {}) or {})
            item_id = str(batch_data.get("item_id", "") or "").strip()
            if item_id == "" or quantity <= 0:
                continue
            if current_day >= ready_day:
                player.add_item(item_id, quantity)
                released += quantity
            else:
                remaining_pending.append({
                    "item_id": item_id,
                    "quantity": quantity,
                    "ready_day": ready_day,
                    "profile": profile,
                })
        crafting.pending_soap_batches = remaining_pending
        return released

    def upstairs_room_search_done(room_code):
        room_key = str(room_code or "").strip()
        room = rooms.get(room_key)
        return bool(room is not None and room.state.get("searched", False))

    def upstairs_room_mark_searched(room_code):
        room_key = str(room_code or "").strip()
        room = rooms.get(room_key)
        if room is not None:
            room.state["searched"] = True

    def upstairs_room_search_text(room_code):
        room_key = str(room_code or "").strip()
        if upstairs_room_search_done(room_key):
            return "Вы уже осматривали эту комнату. Ничего нового в глаза не бросается."
        if room_key == "TavernAmandaRoom":
            return "Вы внимательнее осматриваете комнату Аманды. Под кроватью и возле ларей обнаруживается обычная девичья мелочь, а у ночного столика стоит ночная посудина."
        if room_key == "TavernSandraRoom":
            return "Вы осматриваете комнату Сандры. Здесь все сложено аккуратно, так что поиски не приносят ничего, кроме уважения к ее хозяйственности."
        if room_key == "TavernMelissaRoom":
            if int(effective_player_exploration() or 0) >= 100 and 2 <= threads["melissaBatProblem"].num < 3:
                return "Вы осматриваете комнату Мелиссы внимательнее и замечаете под самым потолком несколько совсем маленьких щелей и норок в старом дереве. Оттуда тянет пылью и затхлым чердаком. Похоже, часть дряни лезет сюда не из самой комнаты, а сверху, через старую крышу и балки."
            if 3 <= threads["melissaBatProblem"].num < 4:
                return "Теперь, когда вы знаете про щели под крышей, становится ясно: без осмотра чердака над комнатой Мелиссы эта история не закончится."
            if 4 <= threads["melissaBatProblem"].num < 8:
                return "Вы еще раз осматриваете комнату Мелиссы и убеждаетесь, что без чистки чердака и заделки крыши мелкая дрянь будет возвращаться снова и снова."
            return "Вы осматриваете комнату Мелиссы. Ничего ценного не находится, зато становится ясно, что она старается держать свои пожитки в порядке."
        if room_key == "TavernEmptyRoom":
            return "Вы внимательно осматриваете пустую комнату. В углах только пыль, паутина и несколько забытых щепок."
        return "Вы осматриваете комнату, но не находите ничего важного."

    def amanda_night_bowl_available(_obj=None):
        return (
            str(rooms.current_code or "") == "TavernAmandaRoom"
            and int(calendar_v2.time_slot() or 0) < 4
            and not Amanda.has_given_night_bowl()
        )

    RecipeBookItem = GameItem(
        object_id="recipe_book_001",
        name="очень старая книга с рецептами",
        description="Очень старая книга с пометками на полях и хозяйственными рецептами.",
        actions=[
            ObjectAction(
                action_id="read_recipe_book",
                label="Прочитать книгу",
                hook="call",
                target="ReadRecipeBook",
                args=("recipe_book_001", "TavernAtic", "", "recipe_book_001"),
            ),
            ObjectAction(
                action_id="take_recipe_book",
                label="Взять книгу",
                hook="call",
                target="Take",
                args=("recipe_book_001", "TavernAtic", "", "recipe_book_001"),
            ),
        ],
        picture="images/player_room/player_table.png",
        carriable=True,
        readable=True,
        stackable=False,
        custom_properties={
            "item_kind": "readable",
            "recipe_kind": "soap",
        },
    )

    NightBowlItem = GameItem(
        object_id="night_bowl_001",
        name="ночная миска",
        description="Простая, но крепкая ночная миска, которую можно пустить на хозяйственные нужды.",
        carriable=True,
        stackable=False,
        condition=amanda_night_bowl_available,
        custom_properties={
            "item_kind": "container",
            "container_kind": "bowl",
        },
    )

    FancyNightBowlItem = GameItem(
        object_id="fancy_night_bowl_001",
        name="красивая ночная миска",
        description="Аккуратная расписная ночная миска из хорошей глины. Вещь не роскошная, но заметно приятнее простой хозяйственной посудины.",
        price=9,
        carriable=True,
        stackable=False,
        custom_properties={
            "item_kind": "container",
            "container_kind": "bowl",
            "gift_value": 1,
        },
    )

    BucketItem = GameItem(
        object_id="bucket_001",
        name="ведро",
        description="Крепкое деревянное ведро для воды, золы и прочих хозяйственных дел.",
        carriable=True,
        stackable=False,
        custom_properties={
            "item_kind": "container",
            "container_kind": "bucket",
            "spawn_zones": ["Сарай"],
            "spawn_rarity": "после тщательных поисков",
        },
    )

    EmptyBottleItem = GameItem(
        object_id="empty_bottle_001",
        name="пустая бутылка",
        description="Пустая стеклянная бутылка. Если ее как следует отмыть, в хозяйстве ей найдется применение.",
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "container",
            "container_kind": "bottle",
            "spawn_zones": ["Портовые переулки"],
            "spawn_rarity": "иногда",
        },
    )

    CorkItem = GameItem(
        object_id="cork_001",
        name="пробка",
        description="Обычная пробка для бутылки. Небольшая вещь, но в хозяйстве бывает очень кстати.",
        price=1,
        carriable=True,
        stackable=True,
        usable=True,
        actions=[
            ObjectAction(
                action_id="use_cork",
                label="Использовать пробку",
                hook="call",
                target="AtticInventoryUseCork",
            ),
        ],
        custom_properties={
            "item_kind": "container_part",
            "part_kind": "cork",
        },
    )

    PigLardItem = GameItem(
        object_id="pig_lard_001",
        name="свиное сало",
        description="Топленое свиное сало, годное и в стряпню, и в мыловарение.",
        price=5,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "ingredient",
            "ingredient_kind": "lard",
        },
    )

    DriedMossItem = GameItem(
        object_id="dried_moss_001",
        name="сушеный мох",
        description="Высушенный и перетертый мох. Его можно пустить на перевязку, зелья или более опасные смеси.",
        price=6,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "ingredient",
            "ingredient_kind": "dried_moss",
        },
    )

    ClothScrapItem = GameItem(
        object_id="cloth_scrap_001",
        name="лоскут ткани",
        description="Полоса мягкой ткани, выдранная из старой одежды. Пригодится для бинтов, веревки и прочих хозяйственных поделок.",
        price=1,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "ingredient",
            "ingredient_kind": "cloth_scrap",
        },
    )

    SoapItem = GameItem(
        object_id="soap_001",
        name="лавандовое хозяйственное мыло",
        description="Кусок домашнего мыла с чистым лавандовым запахом.",
        price=4,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafted_good",
            "crafted_kind": "soap",
            "soap_aroma": "lavender",
            "social_effect_family": "soap",
            "gift_value": 1,
            "attraction_bonus": 1,
        },
    )

    LavenderHerbalSoapItem = GameItem(
        object_id="lavender_herbal_soap_001",
        name="лавандово-травяное мыло",
        description="Домашнее мыло с лавандой и редкими душистыми травами. Именно такой терпкий запах любит Сандра.",
        price=9,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafted_good",
            "crafted_kind": "soap",
            "soap_aroma": "lavender_herbal",
            "social_effect_family": "soap",
            "gift_value": 2,
            "attraction_bonus": 1,
        },
    )

    LavenderRoseSoapItem = GameItem(
        object_id="lavender_rose_soap_001",
        name="лавандово-розовое мыло",
        description="Душистое домашнее мыло, в котором лаванда смешана с мягким ароматом дикой розы. Такой запах особенно нравится Мелиссе.",
        price=10,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafted_good",
            "crafted_kind": "soap",
            "soap_aroma": "lavender_rose",
            "social_effect_family": "soap",
            "gift_value": 2,
            "attraction_bonus": 1,
        },
    )

    RoseHoneySoapItem = GameItem(
        object_id="rose_honey_soap_001",
        name="розово-медовое мыло",
        description="Мягкое домашнее мыло с дикой розой и теплой медовой сладостью. Аманда как раз любит такие яркие запахи.",
        price=10,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafted_good",
            "crafted_kind": "soap",
            "soap_aroma": "rose_honey",
            "social_effect_family": "soap",
            "gift_value": 2,
            "attraction_bonus": 1,
        },
    )

    OliveOilItem = GameItem(
        object_id="olive_oil_001",
        name="оливковое масло",
        description="Маленький пузырек хорошего оливкового масла. Его можно пустить в дело у цирюльника или в более тонкие хозяйственные смеси.",
        price=11,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "ingredient",
            "ingredient_kind": "olive_oil",
        },
    )

    LuxurySoapItem = GameItem(
        object_id="luxury_soap_001",
        name="роскошное мыло",
        description="Брусок улучшенного мыла, в которое втерли оливковое масло. Оно пахнет мягче, выглядит дороже и ценится выше обычного домашнего.",
        price=18,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafted_good",
            "crafted_kind": "soap",
            "soap_grade": "luxury",
            "soap_aroma": "lavender_olive",
            "social_effect_family": "luxury_soap",
            "gift_value": 2,
            "attraction_bonus": 2,
            "social_fun_bonus": 1,
            "social_openness_bonus": 1,
        },
    )

    EthanolItem = GameItem(
        object_id="ethanol_001",
        name="бутылка крепкого спирта",
        description="Плотно укупоренная бутылка с резко пахнущим крепким настоем. Годится для некоторых смесей и хозяйственных опытов.",
        price=10,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "ingredient",
            "ingredient_kind": "ethanol",
            "gift_value": 1,
            "social_fun_bonus": 1,
            "social_openness_bonus": 1,
        },
    )

    EnergyTeaItem = GameItem(
        object_id="energy_tea_001",
        name="бодрящий чай",
        description="Горячий травяной настой, после которого чувствуешь себя заметно бодрее.",
        price=8,
        carriable=True,
        stackable=True,
        usable=True,
        actions=[
            ObjectAction(
                action_id="drink",
                label="Выпить чай",
                hook="call",
                target="UseDrinkItem",
                args=("energy_tea_001",),
            ),
        ],
        custom_properties={
            "item_kind": "drink",
            "drink_kind": "energy_tea",
            "consume_action": "drink",
            "consume_minutes": 30,
            "consume_energy": 20,
            "fight_speed_boost": 4,
            "consume_fun": 0,
            "consume_text": "Вы выпиваете крепкий бодрящий чай. Тело понемногу отпускает усталость, а в голове проясняется. После этого у вас остаются пустая бутылка и пробка.",
            "consume_outputs": (("empty_bottle_001", 1), ("cork_001", 1)),
            "gift_value": 1,
            "social_fun_bonus": 1,
            "social_openness_bonus": 1,
        },
    )

    LibidoTinctureItem = GameItem(
        object_id="libido_tincture_001",
        name="пряная настойка",
        description="Небольшая бутылка сладковатой пряной настойки. Ее можно выпить, подарить или продать, а за дружеским столом она быстро развязывает язык.",
        price=14,
        carriable=True,
        stackable=True,
        usable=True,
        actions=[
            ObjectAction(
                action_id="drink",
                label="Выпить настойку",
                hook="call",
                target="UseDrinkItem",
                args=("libido_tincture_001",),
            ),
        ],
        custom_properties={
            "item_kind": "drink",
            "drink_kind": "libido_tincture",
            "consume_action": "drink",
            "consume_minutes": 40,
            "consume_energy": 8,
            "consume_fun": 8,
            "consume_text": "Пряная настойка мягко ударяет в голову, разогревает кровь и заметно развязывает язык. После этого у вас остаются пустая бутылка и пробка.",
            "consume_outputs": (("empty_bottle_001", 1), ("cork_001", 1)),
            "gift_value": 2,
            "social_friend_bonus": 1,
            "social_fun_bonus": 3,
            "social_openness_bonus": 2,
            "social_trust_bonus": 1,
            "social_horny_bonus": 1,
        },
    )

    SpecialCreamItem = GameItem(
        object_id="special_cream_001",
        name="особая смягчающая мазь",
        description="Плотная душистая мазь по рецепту Серджио. Ее можно использовать как дорогой подарок или мягкое средство ухода.",
        price=20,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafted_good",
            "crafted_kind": "special_cream",
            "gift_value": 3,
            "social_friend_bonus": 1,
            "social_openness_bonus": 2,
            "social_trust_bonus": 1,
            "intimacy_helper": 1,
        },
    )

    FireBombItem = GameItem(
        object_id="fire_bomb_001",
        name="огненная бутылка",
        description="Бутылка с масляно-спиртовой смесью и сухим мхом. В драке это грубое, но действенное зажигательное средство.",
        price=18,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "hunter_supply",
            "supply_kind": "fire_bomb",
        },
    )

    BatRepellentItem = GameItem(
        object_id="bat_repellent_001",
        name="дымная смесь от мышей и летучих тварей",
        description="Бутылка с едкой душной смесью из сушеного мха, лаванды и трав. Если разжечь ее в тесном чердаке, мерзкая пакость там долго не усидит.",
        price=18,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafted_good",
            "crafted_kind": "bat_repellent",
            "supply_kind": "smoke_mix",
        },
    )

    AshBarrelItem = GameItem(
        object_id="ash_barrel_001",
        name="зольная бочка с дырчатым дном",
        description="Специальная бочка для приготовления щелока из золы.",
        carriable=False,
        stackable=False,
        custom_properties={
            "item_kind": "soap_tool",
            "tool_kind": "ash_barrel",
        },
    )

    RustyHunterRifleItem = GameItem(
        object_id="rusty_hunter_rifle_001",
        name="ржавая охотничья винтовка-арбалет",
        description="Старинная помесь ружья и арбалета. Сейчас она слишком ржавая для уверенного применения, но выглядит занятно.",
        actions=[
            ObjectAction(
                action_id="take_rusty_rifle",
                label="Забрать оружие",
                hook="call",
                target="Take",
                args=("rusty_hunter_rifle_001", "TavernAtic", "", "rusty_hunter_rifle_001"),
            ),
        ],
        picture="images/player_room/rifle0.png",
        carriable=True,
        stackable=False,
        weapon=True,
        custom_properties={
            "item_kind": "weapon",
            "weapon_kind": "hybrid_rifle",
            "attack_points": 14,
            "speed_penalty": 2,
            "ammo_kind": "arbalest_bolt",
            "can_bleed": True,
        },
    )

    OldLeatherCuirassItem = GameItem(
        object_id="old_leather_cuirass_001",
        name="старый кожаный кирас",
        description="Старая кожаная кираса с потемневшими ремнями. Защита уже не новая, но все еще годная.",
        actions=[
            ObjectAction(
                action_id="take_old_cuirass",
                label="Забрать кирасу",
                hook="call",
                target="Take",
                args=("old_leather_cuirass_001", "TavernAtic", "", "old_leather_cuirass_001"),
            ),
        ],
        picture="images/tavern/backyard/cuirass.png",
        carriable=True,
        stackable=False,
        wearable=True,
        custom_properties={
            "item_kind": "armor",
            "armor_kind": "leather_cuirass",
            "armor_slot": "body",
            "armor_points": 8,
            "defence_points": 8,
            "speed_penalty": 3,
        },
    )

    SoapRecipePage = SoapBatchRecipePage(
        recipe_id="soap_recipe",
        title="Лавандовое хозяйственное мыло",
        image="images/recipe_book/soap_recipe.png",
        item_result="soap_001",
        ingredients=soap_recipe_ingredients("lavender_001"),
        unlocked=False,
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=4,
        craft_minutes=120,
        craft_text="Вы варите партию мыла и раскладываете ее по формам.",
        craft_failure_text="Не удалось взять нужные вещи для мыла.",
        notes=[
            "Варить мыло лучше во дворе, где есть огонь и место для большой посуды.",
            "Щелок готовится неделю, а сваренная партия вылеживается еще неделю.",
            "Оливковое масло лучше пустить в отдельную туалетную партию, а не в хозяйственное мыло.",
        ],
    )

    LavenderHerbalSoapRecipePage = SoapBatchRecipePage(
        recipe_id="lavender_herbal_soap_recipe",
        title="Лавандово-травяное мыло",
        image="images/recipe_book/soap_recipe.png",
        item_result="lavender_herbal_soap_001",
        ingredients=soap_recipe_ingredients("lavender_001", "special_herbs_001"),
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=4,
        craft_minutes=120,
        craft_failure_text="Не удалось взять нужные вещи для лавандово-травяного мыла.",
        notes=["Терпкий лавандово-травяной запах особенно нравится Сандре."],
    )

    LavenderRoseSoapRecipePage = SoapBatchRecipePage(
        recipe_id="lavender_rose_soap_recipe",
        title="Лавандово-розовое мыло",
        image="images/recipe_book/soap_recipe.png",
        item_result="lavender_rose_soap_001",
        ingredients=soap_recipe_ingredients("lavender_001", "wild_rose_001"),
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=4,
        craft_minutes=120,
        craft_failure_text="Не удалось взять нужные вещи для лавандово-розового мыла.",
        notes=["Сочетание лаванды и дикой розы особенно нравится Мелиссе."],
    )

    RoseHoneySoapRecipePage = SoapBatchRecipePage(
        recipe_id="rose_honey_soap_recipe",
        title="Розово-медовое мыло",
        image="images/recipe_book/soap_recipe.png",
        item_result="rose_honey_soap_001",
        ingredients=soap_recipe_ingredients("wild_rose_001", "honey_comb_001"),
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=4,
        craft_minutes=120,
        craft_failure_text="Не удалось взять нужные вещи для розово-медового мыла.",
        notes=["Яркий запах розы с медовой сладостью особенно нравится Аманде."],
    )

    LuxurySoapRecipePage = SoapBatchRecipePage(
        recipe_id="luxury_soap_recipe",
        title="Лавандовое туалетное мыло с оливковым маслом",
        image="images/recipe_book/soap_recipe.png",
        item_result="luxury_soap_001",
        ingredients=soap_recipe_ingredients("lavender_001", "olive_oil_001"),
        unlocked=False,
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=4,
        craft_minutes=120,
        craft_text="Вы варите партию туалетного мыла и раскладываете ее по формам.",
        craft_failure_text="Не удалось взять нужные вещи для туалетного мыла.",
        notes=[
            "Это мыло годится для купания, ухода и подарков, а не только для хозяйственных нужд.",
            "Щелок готовится неделю, а сваренная партия вылеживается еще неделю.",
        ],
    )

    TorchRecipePage = RecipePage(
        recipe_id="torch_recipe",
        title="Факел",
        image="images/recipe_book/torch_recipe.png",
        item_result="torch_001",
        ingredients={
            "lumber_001": {"quantity": 1, "unit": "полено"},
            "rope_001": {"quantity": 1, "unit": "моток"},
            "honey_comb_001": {"quantity": 1, "unit": "кусок"},
        },
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=1,
        craft_minutes=30,
        craft_text="Вы обматываете палку вощеной веревкой и получаете надежный факел.",
        craft_failure_text="Не удалось взять материалы для факела.",
        notes=[
            "Вощеная обмотка и крепкая палка позволяют сделать простой, но надежный факел.",
        ],
    )

    EthanolRecipePage = RecipePage(
        recipe_id="ethanol_recipe",
        title="Крепкий спирт",
        image="images/recipe_book/ethanol_recipe.png",
        item_result="ethanol_001",
        ingredients={
            "berries_001": {"quantity": 2, "unit": "горсть"},
            "honey_comb_001": {"quantity": 1, "unit": "кусок"},
            "bucket_001": {"quantity": 1, "unit": "штука", "consume": False},
            "empty_bottle_001": {"quantity": 1, "unit": "бутылка"},
        },
        unlock_condition=soap_recipe_chain_discovered,
        result_quantity=1,
        craft_minutes=90,
        craft_text="Вы давите ягоды, смешиваете их с медом и аккуратно переливаете получившийся крепкий спирт в бутылку.",
        craft_failure_text="Не удалось взять ингредиенты для спирта.",
        notes=[
            "Сладкая ягодная брага дает крепкий настой, если с ней не торопиться.",
            "Готовый спирт лучше сразу перелить в пустую бутылку.",
        ],
    )

    EnergyTeaRecipePage = RecipePage(
        recipe_id="energy_tea_recipe",
        title="Бодрящий чай",
        image="images/recipe_book/energy_tea_recipe.png",
        item_result="energy_tea_001",
        ingredients={
            "special_herbs_001": {"quantity": 1, "unit": "пучок"},
            "mushroom_001": {"quantity": 1, "unit": "щепоть"},
            "honey_comb_001": {"quantity": 1, "unit": "кусок"},
            "bucket_001": {"quantity": 1, "unit": "штука", "consume": False},
        },
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=1,
        craft_minutes=30,
        craft_text="Вы завариваете редкие травы с грибной щепотью и медовой сладостью. Настой выходит терпким, но бодрящим, и у вас получается порция бодрящего чая.",
        craft_failure_text="Не удалось взять ингредиенты для чая.",
        notes=[
            "Правильно заваренные травы и немного медовой сладости хорошо снимают усталость.",
        ],
    )

    LibidoRecipePage = LibidoTinctureRecipePage(
        recipe_id="libido_recipe",
        title="Пряная настойка",
        image="images/recipe_book/libido_recipe.png",
        item_result="libido_tincture_001",
        ingredients={
            "ethanol_001": {"quantity": 1, "unit": "бутылка"},
            "honey_comb_001": {"quantity": 1, "unit": "кусок"},
            "flavor_mix": {
                "quantity": 1,
                "unit": "порция",
                "alternatives": ["special_herbs_001", "berries_001"],
                "note": "Для вкуса берут терпкие травы или сладкие ягоды.",
            },
        },
        unlock_condition=soap_recipe_chain_discovered,
        result_quantity=1,
        craft_minutes=50,
        craft_text="Вы смешиваете крепкий спирт с медом и добавляете {}. Напиток получается мягким и пряным.",
        craft_failure_text="Не удалось взять ингредиенты для настойки.",
        notes=[
            "Такая настойка уже годится не только для хозяйства, но и для дружеских разговоров.",
            "После пары глотков люди обычно становятся заметно разговорчивее и смелее.",
        ],
    )

    SpecialCreamRecipePage = RecipePage(
        recipe_id="special_cream_recipe",
        title="Особая смягчающая мазь Серджио",
        image="images/recipe_book/soap_recipe.png",
        item_result="special_cream_001",
        ingredients={
            "olive_oil_001": {"quantity": 1, "unit": "пузырек"},
            "pig_lard_001": {"quantity": 1, "unit": "кусок"},
            "flavor_mix": {
                "quantity": 1,
                "unit": "порция",
                "alternatives": ["lavender_001", "wild_rose_001", "special_herbs_001"],
                "note": "Для запаха и мягкости подойдет лаванда, дикая роза или редкие травы.",
            },
        },
        unlock_condition=lambda: bool(crafting.special_cream_recipe_unlocked),
        result_quantity=1,
        notes=[
            "Серджио записал рецепт после того, как его отпустили по делу столичного жениха.",
            "Мазь годится для ухода, подарков и дальнейших интимных сцен, если они открыты сюжетом.",
        ],
    )

    DryMossRecipePage = RecipePage(
        recipe_id="dry_moss_recipe",
        title="Сушеный мох",
        image="images/recipe_book/recipe_book_attick.png",
        item_result="dried_moss_001",
        ingredients={
            "moss_001": {"quantity": 1, "unit": "пучок"},
        },
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=1,
        craft_minutes=30,
        craft_text="Вы раскладываете сырой мох в сухом месте, даете ему как следует подсохнуть и перетираете его в сухую крошку. Получается заготовка для дальнейших смесей.",
        craft_failure_text="Не удалось взять сырой мох.",
        notes=[
            "Сырой мох сперва надо хорошо просушить, иначе он только испортит смесь.",
        ],
    )

    MossGunpowderRecipePage = RecipePage(
        recipe_id="moss_gunpowder_recipe",
        title="Порох из сушеного мха",
        image="images/recipe_book/recipe_book_attick.png",
        item_result="gunpowder_001",
        ingredients={
            "dried_moss_001": {"quantity": 3, "unit": "порции"},
        },
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=1,
        craft_minutes=40,
        craft_text="Вы мелко перетираете высушенный мох и доводите смесь до плотного темного порошка. Получается самодельный пороховой заряд.",
        craft_failure_text="Не удалось взять сушеный мох.",
        notes=[
            "Из хорошо высушенного мха выходит грубый, но годный порошок для старого охотничьего снаряжения.",
        ],
    )

    HealingPotionRecipePage = RecipePage(
        recipe_id="healing_potion_recipe",
        title="Лечебное зелье",
        image="images/recipe_book/recipe_book_attick.png",
        item_result="healing_potion_001",
        ingredients={
            "dried_moss_001": {"quantity": 2, "unit": "порции"},
            "special_herbs_001": {"quantity": 1, "unit": "пучок"},
            "bucket_001": {"quantity": 1, "unit": "ведро", "consume": False, "note": "Нужно для горячей воды."},
            "empty_bottle_001": {"quantity": 1, "unit": "бутылка"},
        },
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=1,
        craft_minutes=45,
        craft_text="Вы заливаете сушеный мох горячей водой, добавляете редкие травы и даете настою набрать силу. После этого аккуратно разливаете лечебный отвар по бутылке.",
        craft_failure_text="Не удалось взять ингредиенты для зелья.",
        notes=[
            "Сушеный мох и редкие травы дают густой лечебный отвар, если заварить их в горячей воде.",
        ],
    )

    BandageRecipePage = RecipePage(
        recipe_id="bandage_recipe",
        title="Перевязочный бинт",
        image="images/recipe_book/recipe_book_attick.png",
        item_result="bandage_001",
        ingredients={
            "cloth_scrap_001": {"quantity": 1, "unit": "лоскут"},
            "dried_moss_001": {"quantity": 1, "unit": "порция"},
        },
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=1,
        craft_minutes=20,
        craft_text="Вы сворачиваете лоскут ткани с сухим мхом и получаете простой, но полезный перевязочный бинт.",
        craft_failure_text="Не удалось взять материалы для бинта.",
        notes=[
            "Чистый лоскут и сухой мох дают простую, но полезную перевязку.",
        ],
    )

    ClothRopeRecipePage = RecipePage(
        recipe_id="cloth_rope_recipe",
        title="Веревка из лоскутов",
        image="images/recipe_book/recipe_book_attick.png",
        item_result="rope_001",
        ingredients={
            "cloth_scrap_001": {"quantity": 5, "unit": "лоскутов"},
        },
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=1,
        craft_minutes=40,
        craft_text="Вы долго скручиваете полосы ткани в плотный жгут, пока из них не выходит крепкая хозяйственная веревка.",
        craft_failure_text="Не удалось взять лоскуты для веревки.",
        notes=[
            "Если ткани накопилось достаточно, ее можно пустить на грубую, но крепкую веревку.",
        ],
    )

    FireBombRecipePage = RecipePage(
        recipe_id="fire_bomb_recipe",
        title="Огненная бутылка",
        image="images/recipe_book/recipe_book_attick.png",
        item_result="fire_bomb_001",
        ingredients={
            "weapon_oil_001": {"quantity": 1, "unit": "пузырек"},
            "ethanol_001": {"quantity": 1, "unit": "бутылка"},
            "dried_moss_001": {"quantity": 3, "unit": "порции"},
            "empty_bottle_001": {"quantity": 1, "unit": "бутылка"},
        },
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=1,
        craft_minutes=30,
        craft_text="Вы смешиваете масло со спиртом, добавляете сухой мох и плотно набиваете этим бутылку. Получается огненная бутылка, которую лучше держать подальше от открытого огня.",
        craft_failure_text="Не удалось взять ингредиенты для огненной бутылки.",
        notes=[
            "Это уже не хозяйственная поделка, а грубое зажигательное оружие.",
        ],
    )

    BatRepellentRecipePage = RecipePage(
        recipe_id="bat_repellent_recipe",
        title="Дымная смесь от летучих тварей",
        image="images/recipe_book/recipe_book_attick.png",
        item_result="bat_repellent_001",
        ingredients={
            "dried_moss_001": {"quantity": 1, "unit": "порция"},
            "special_herbs_001": {"quantity": 1, "unit": "пучок"},
            "lavender_001": {"quantity": 1, "unit": "веточка"},
            "empty_bottle_001": {"quantity": 1, "unit": "бутылка"},
        },
        unlock_condition=recipe_book_hidden_recipes_revealed,
        result_quantity=1,
        craft_minutes=35,
        craft_text="Вы перетираете сушеный мох с лавандой и редкими травами, завариваете густую душную смесь и разливаете ее в бутылку. Получается едкий дымный состав, которым можно выкуривать дрянь из-под крыши.",
        craft_failure_text="Не удалось взять ингредиенты для дымной смеси.",
        notes=[
            "Смесь годится не для лечения, а чтобы выкуривать из-под крыши мелкую дрянь и летучих тварей.",
        ],
    )


default crafting = CraftingInfo()


label AtticInventoryMenu(return_context="attic", room_code="TavernAtic"):
    $ renpy.dynamic("_item_id")
    $ main_ui_runtime.action_title = "Вещи"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    python:
        for _item_id in attic_manageable_item_ids():
            if player.item_count(_item_id) > 0:
                main_ui_runtime.action_items.append(MenuItem(attic_item_menu_caption(_item_id), Call("AtticInventoryItemMenu", _item_id, return_context, room_code)))
        if len(main_ui_runtime.action_items) <= 0:
            scene_runtime.text = "Сейчас у вас нет найденных на чердаке вещей при себе."
            scene_runtime.location_text = scene_runtime.text
        if str(return_context or "") == "chest":
            main_ui_runtime.action_items.append(MenuItem("Назад", Call("TavernMyRoomOpenChest")))
        else:
            main_ui_runtime.action_items.append(MenuItem("Назад", [
                SetField(main_ui_runtime, "action_title", "Действия"),
                SetField(main_ui_runtime, "action_content", None),
                SetField(main_ui_runtime, "action_items", tavern_atic_action_items()),
                Function(main_ui_restart_interaction),
            ]))
    return


label AtticInventoryItemMenu(item_id="", return_context="attic", room_code="TavernAtic", preserve_text=False):
    $ renpy.dynamic("_item_id", "_item_obj", "_status_text")
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or player.item_count(_item_id) <= 0:
        call AtticInventoryMenu(return_context, room_code)
        return
    $ _status_text = attic_item_equipped_text(_item_id)
    if not bool(preserve_text):
        if str(_status_text or "").strip() != "":
            $ scene_runtime.text = runtime_item_description_text(_item_id) + "\n\n" + str(_status_text or "")
        else:
            $ scene_runtime.text = runtime_item_description_text(_item_id)
        if _item_id == "rusty_hunter_rifle_001":
            $ scene_runtime.text = str(scene_runtime.text or "") + "\n\n" + "\n".join(rusty_hunter_rifle_status_lines())
        $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = runtime_item_display_name(_item_id) or str(_item_obj.name or "Вещь")
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    if bool(getattr(_item_obj, "readable", False)):
        $ main_ui_runtime.action_items.append(MenuItem("Прочитать", Call("AtticInventoryReadItem", _item_id, return_context, room_code)))
    if player_can_use_soap(_item_id):
        $ main_ui_runtime.action_items.append(MenuItem("Использовать мыло", Call("AtticInventoryUseSoap", _item_id, return_context, room_code)))
    if _item_id == "cork_001":
        $ main_ui_runtime.action_items.append(MenuItem("Использовать пробку", Call("AtticInventoryUseCork", _item_id, return_context, room_code)))
    if _item_id == "rusty_hunter_rifle_001":
        if rusty_hunter_rifle_can_clean():
            $ main_ui_runtime.action_items.append(MenuItem("Счистить ржавчину", Call("AtticInventoryRifleCleanRust", return_context, room_code)))
        if rusty_hunter_rifle_can_oil():
            $ main_ui_runtime.action_items.append(MenuItem("Смазать механизм", Call("AtticInventoryRifleOil", return_context, room_code)))
        if rusty_hunter_rifle_can_load("arrows"):
            $ main_ui_runtime.action_items.append(MenuItem("Зарядить стрелой", Call("AtticInventoryRifleLoadAmmo", "arrows", return_context, room_code)))
        if rusty_hunter_rifle_can_load("droplets"):
            $ main_ui_runtime.action_items.append(MenuItem("Зарядить дробью", Call("AtticInventoryRifleLoadAmmo", "droplets", return_context, room_code)))
        if rusty_hunter_rifle_can_unload():
            $ main_ui_runtime.action_items.append(MenuItem("Разрядить оружие", Call("AtticInventoryRifleUnload", return_context, room_code)))
    if str(_item_id) == str(player.equipment.weapon or ""):
        $ main_ui_runtime.action_items.append(MenuItem("Убрать оружие", Call("AtticInventoryUnequipItem", _item_id, return_context, room_code)))
    elif str(getattr(_item_obj, "custom_properties", {}).get("item_kind", "") or "") == "weapon":
        $ main_ui_runtime.action_items.append(MenuItem("Вооружиться", Call("AtticInventoryEquipItem", _item_id, return_context, room_code)))
    if str(_item_id) == str(player.equipment.armor or ""):
        $ main_ui_runtime.action_items.append(MenuItem("Снять", Call("AtticInventoryUnequipItem", _item_id, return_context, room_code)))
    elif str(getattr(_item_obj, "custom_properties", {}).get("item_kind", "") or "") == "armor":
        $ main_ui_runtime.action_items.append(MenuItem("Надеть", Call("AtticInventoryEquipItem", _item_id, return_context, room_code)))
    $ main_ui_runtime.action_items.append(MenuItem("Оставить здесь", Call("AtticInventoryDropItem", _item_id, return_context, room_code)))
    $ main_ui_runtime.action_items.append(MenuItem("Назад", Call("AtticInventoryMenu", return_context, room_code)))
    return


label AtticInventoryReadItem(item_id="", return_context="attic", room_code="TavernAtic"):
    $ renpy.dynamic("_item_id")
    $ _item_id = str(item_id or "").strip()
    if _item_id == "recipe_book_001":
        $ scene_runtime.text = recipe_book_read_text()
        $ scene_runtime.location_text = scene_runtime.text
    call AtticInventoryItemMenu(_item_id, return_context, room_code, True)
    return


label AtticInventoryEquipItem(item_id="", return_context="attic", room_code="TavernAtic"):
    $ renpy.dynamic("_item_id", "_item_obj")
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or player.item_count(_item_id) <= 0:
        call AtticInventoryMenu(return_context, room_code)
        return
    if str(getattr(_item_obj, "custom_properties", {}).get("item_kind", "") or "") == "weapon":
        $ player.equipment.weapon = _item_id
        $ scene_runtime.text = "Вы берете при себе " + runtime_item_display_name(_item_id) + "."
    elif str(getattr(_item_obj, "custom_properties", {}).get("item_kind", "") or "") == "armor":
        $ player.equipment.armor = _item_id
        $ scene_runtime.text = "Вы надеваете " + runtime_item_display_name(_item_id) + "."
    else:
        $ scene_runtime.text = "Сейчас это нельзя надеть."
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call AtticInventoryItemMenu(_item_id, return_context, room_code, True)
    return


label AtticInventoryUnequipItem(item_id="", return_context="attic", room_code="TavernAtic"):
    $ renpy.dynamic("_item_id", "_item_obj")
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None:
        call AtticInventoryMenu(return_context, room_code)
        return
    if _item_id == str(player.equipment.weapon or ""):
        $ player.equipment.weapon = ""
        $ scene_runtime.text = "Вы убираете " + str(_item_obj.name or _item_id) + "."
    elif _item_id == str(player.equipment.armor or ""):
        $ player.equipment.armor = ""
        $ scene_runtime.text = "Вы снимаете " + str(_item_obj.name or _item_id) + "."
    else:
        $ scene_runtime.text = "Сейчас это и так не надето."
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call AtticInventoryItemMenu(_item_id, return_context, room_code, True)
    return


label AtticInventoryDropItem(item_id="", return_context="attic", room_code="TavernAtic"):
    $ renpy.dynamic("_item_id", "_item_obj", "_drop_result")
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_id == str(player.equipment.weapon or ""):
        $ player.equipment.weapon = ""
    if _item_id == str(player.equipment.armor or ""):
        $ player.equipment.armor = ""
    $ _drop_result = player_drop_item(rooms.current, _item_id)
    if _drop_result.get("ok", False):
        if _item_obj is not None:
            $ scene_runtime.text = "Вы оставляете здесь " + str(_item_obj.name or _item_id) + "."
        else:
            $ scene_runtime.text = str(_drop_result.get("text", "") or "Вы оставляете предмет здесь.")
    else:
        $ scene_runtime.text = str(_drop_result.get("text", "") or "У вас этого нет.")
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    call AtticInventoryMenu(return_context, room_code)
    return


label AtticInventoryUseSoap(item_id="", return_context="attic", room_code="TavernAtic"):
    $ renpy.dynamic("_soap_item_id", "_soap_item", "_soap_grade")
    $ _soap_item_id = str(item_id or "").strip()
    $ _soap_item = get_game_item(_soap_item_id)
    if not player_can_use_soap(_soap_item_id):
        $ scene_runtime.text = "У вас больше не осталось мыла."
        $ scene_runtime.location_text = scene_runtime.text
        call AtticInventoryMenu(return_context, room_code)
        return
    $ _soap_grade = str(getattr(_soap_item, "custom_properties", {}).get("soap_grade", "ordinary") or "ordinary")
    $ player.remove_item(_soap_item_id, 1)
    $ player.appearance.wash_with_soap(current_game_day(), 10 if _soap_grade == "luxury" else 5, 2 if _soap_grade == "luxury" else 1)
    $ player.change_stat("fun", 2)
    call stat
    $ scene_runtime.text = "Вы тщательно моетесь, используя {}. Кожа становится чище, запах приятнее, а выглядите вы заметно лучше. Чистота и свежесть еще какое-то время будут работать на ваш вид.".format(str(getattr(_soap_item, "name", "душистое мыло") or "душистое мыло"))
    if player.item_count(_soap_item_id) <= 0:
        $ scene_runtime.text = scene_runtime.text + "\n\nЭто был последний такой кусок мыла."
    $ scene_runtime.location_text = scene_runtime.text
    call AtticInventoryMenu(return_context, room_code)
    return


label AtticInventoryUseCork(item_id="", return_context="attic", room_code="TavernAtic"):
    if int(player.item_count("cork_001") or 0) <= 0:
        $ scene_runtime.text = "У вас сейчас нет пробки."
        $ scene_runtime.location_text = scene_runtime.text
        call AtticInventoryMenu(return_context, room_code)
        return
    if int(player.item_count("empty_bottle_001") or 0) <= 0 and int(player.item_count("ethanol_001") or 0) <= 0:
        $ scene_runtime.text = "Пробку пока не к чему применить. У вас нет под рукой подходящей бутылки."
        $ scene_runtime.location_text = scene_runtime.text
        call AtticInventoryMenu(return_context, room_code)
        return
    $ player.remove_item("cork_001", 1)
    $ scene_runtime.text = "Вы плотно затыкаете бутылку пробкой. Теперь содержимое не расплещется по дороге."
    $ scene_runtime.location_text = scene_runtime.text
    call AtticInventoryMenu(return_context, room_code)
    return


label AtticInventoryRifleCleanRust(return_context="attic", room_code="TavernAtic"):
    $ renpy.dynamic("_rifle_item")
    $ _rifle_item = rusty_hunter_rifle_item()
    if _rifle_item is None or player.item_count("rusty_hunter_rifle_001") <= 0:
        call AtticInventoryMenu(return_context, room_code)
        return
    if rusty_hunter_rifle_is_cleaned():
        $ scene_runtime.text = "Вы уже счистили основную ржавчину с механизма."
    else:
        $ _rifle_item.state["rust_cleaned"] = 1
        $ scene_runtime.text = "Вы долго скоблите металл, снимаете рыжий налет и понемногу приводите механизм в порядок. Оружие уже не выглядит совсем уж мертвым."
    $ scene_runtime.location_text = scene_runtime.text
    call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
    return


label AtticInventoryRifleOil(return_context="attic", room_code="TavernAtic"):
    $ renpy.dynamic("_rifle_item")
    $ _rifle_item = rusty_hunter_rifle_item()
    if _rifle_item is None or player.item_count("rusty_hunter_rifle_001") <= 0:
        call AtticInventoryMenu(return_context, room_code)
        return
    if not rusty_hunter_rifle_is_cleaned():
        $ scene_runtime.text = "Сначала нужно счистить ржавчину, иначе толку от масла будет мало."
    elif rusty_hunter_rifle_is_oiled():
        $ scene_runtime.text = "Механизм уже смазан и ходит заметно мягче."
    elif player.item_count("weapon_oil_001") <= 0:
        $ scene_runtime.text = "У вас нет оружейного масла."
    else:
        $ player.remove_item("weapon_oil_001", 1)
        $ _rifle_item.state["oiled"] = 1
        $ scene_runtime.text = "Вы аккуратно смазываете механизм оружейным маслом. Скрип уходит, а детали начинают двигаться куда увереннее."
    $ scene_runtime.location_text = scene_runtime.text
    call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
    return


label AtticInventoryRifleLoadAmmo(ammo_code="arrows", return_context="attic", room_code="TavernAtic"):
    $ renpy.dynamic("_ammo_code")
    $ _ammo_code = str(ammo_code or "").strip()
    if not rusty_hunter_rifle_can_load(_ammo_code):
        $ scene_runtime.text = "Сейчас оружие нельзя так зарядить."
        $ scene_runtime.location_text = scene_runtime.text
        call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
        return
    if _ammo_code == "arrows":
        $ player.remove_item("arrows_001", 1)
    elif _ammo_code == "droplets":
        $ player.remove_item("droplets_001", 1)
        $ player.remove_item("gunpowder_001", 1)
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = _ammo_code
    $ scene_runtime.text = "Вы заряжаете оружие {} и осторожно ставите механизм наготове.".format(rusty_hunter_rifle_ammo_name(_ammo_code))
    $ scene_runtime.location_text = scene_runtime.text
    call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
    return


label AtticInventoryRifleUnload(return_context="attic", room_code="TavernAtic"):
    $ renpy.dynamic("_loaded_ammo")
    $ _loaded_ammo = rusty_hunter_rifle_loaded_ammo()
    if _loaded_ammo == "":
        $ scene_runtime.text = "Оружие и так уже разряжено."
        $ scene_runtime.location_text = scene_runtime.text
        call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
        return
    if _loaded_ammo == "arrows":
        $ player.add_item("arrows_001", 1)
    elif _loaded_ammo == "droplets":
        $ player.add_item("droplets_001", 1)
        $ player.add_item("gunpowder_001", 1)
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = ""
    $ scene_runtime.text = "Вы осторожно разряжаете оружие и убираете заряд."
    $ scene_runtime.location_text = scene_runtime.text
    call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
    return


label UpstairsRoomSearch(room_code=""):
    $ renpy.dynamic("_up_room_code")
    $ _up_room_code = str(room_code or rooms.current_code or "")
    $ findAvailableEvents(True)
    if story_event_available(_up_room_code, "room_search"):
        call checkTriggers(_up_room_code, "room_search", 0)
        return
    $ scene_runtime.text = upstairs_room_search_text(_up_room_code)
    $ scene_runtime.location_text = scene_runtime.text
    $ upstairs_room_mark_searched(_up_room_code)
    return


label BackyardCookSoap(recipe_id="soap_recipe"):
    $ renpy.dynamic("_soap_recipe_id", "_soap_craft_result")
    $ _soap_recipe_id = str(recipe_id or "soap_recipe").strip()
    if not recipe_page_can_craft(_soap_recipe_id):
        $ scene_runtime.text = "У вас нет необходимых ингредиентов, чтобы сварить мыло."
        $ scene_runtime.location_text = scene_runtime.text
        call BackyardObjectMenu("backyard_ash_barrel", True)
        return

    $ _soap_craft_result = apply_recipe_craft(_soap_recipe_id)
    $ scene_runtime.text = str(_soap_craft_result.get("text", "") or "Вы варите мыло.")
    $ scene_runtime.location_text = scene_runtime.text
    call BackyardObjectMenu("backyard_ash_barrel", True)
    return


label BackyardChooseSoapRecipe:
    $ scene_runtime.text = "Вы раскрываете старую книгу на записях о мыловарении и выбираете, какую именно партию сварить. Каждый запах требует своих добавок; ничего из сумки не будет взято без вашего выбора."
    $ scene_runtime.location_text = scene_runtime.text
    show screen main_ui
    menu:
        "Лавандовое хозяйственное мыло":
            call BackyardCookSoap("soap_recipe")

        "Лавандово-травяное мыло":
            call BackyardCookSoap("lavender_herbal_soap_recipe")

        "Лавандово-розовое мыло":
            call BackyardCookSoap("lavender_rose_soap_recipe")

        "Розово-медовое мыло":
            call BackyardCookSoap("rose_honey_soap_recipe")

        "Лавандовое туалетное мыло с оливковым маслом":
            call BackyardCookSoap("luxury_soap_recipe")

        "Назад":
            call BackyardObjectMenu("backyard_ash_barrel", True)
    return


label ShootingPracticeMenu(room_code=""):
    $ renpy.dynamic("_shoot_room_code", "_shoot_return_items")
    $ _shoot_room_code = str(room_code or rooms.current_code or "").strip()
    if _shoot_room_code == "Backyard":
        $ _shoot_return_items = backyard_action_items()
    elif _shoot_room_code == "Forest":
        $ _shoot_return_items = forest_action_items()
    else:
        $ _shoot_return_items = forest_subroom_action_items(rooms.current)
    if not player_can_train_shooting():
        $ scene_runtime.text = "Сейчас вам нечем как следует потренироваться в стрельбе."
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_runtime.action_title = "Действия"
        $ main_ui_runtime.action_content = None
        $ main_ui_runtime.action_items = _shoot_return_items
        return
    $ scene_runtime.text = shooting_practice_intro_text(_shoot_room_code)
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Стрельба"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    if rusty_hunter_rifle_loaded_ammo() != "":
        $ main_ui_runtime.action_items.append(MenuItem("Сделать пробный выстрел ({})".format(rusty_hunter_rifle_ammo_name(rusty_hunter_rifle_loaded_ammo())), Call("ShootingPracticeFire", _shoot_room_code)))
    if rusty_hunter_rifle_can_load("arrows"):
        $ main_ui_runtime.action_items.append(MenuItem("Зарядить стрелой", Call("ShootingPracticeLoadAmmo", "arrows", _shoot_room_code)))
    if rusty_hunter_rifle_can_load("droplets"):
        $ main_ui_runtime.action_items.append(MenuItem("Зарядить дробью", Call("ShootingPracticeLoadAmmo", "droplets", _shoot_room_code)))
    if rusty_hunter_rifle_can_unload():
        $ main_ui_runtime.action_items.append(MenuItem("Разрядить оружие", Call("ShootingPracticeUnload", _shoot_room_code)))
    $ main_ui_runtime.action_items.append(MenuItem("Назад", [SetField(main_ui_runtime, "action_title", "Действия"), SetField(main_ui_runtime, "action_content", None), SetField(main_ui_runtime, "action_items", _shoot_return_items), Function(main_ui_restart_interaction)]))
    return


label ShootingPracticeLoadAmmo(ammo_code="arrows", room_code=""):
    $ renpy.dynamic("_ammo_code")
    $ _ammo_code = str(ammo_code or "").strip()
    if not rusty_hunter_rifle_can_load(_ammo_code):
        $ scene_runtime.text = "Сейчас оружие нельзя так зарядить."
        $ scene_runtime.location_text = scene_runtime.text
        call ShootingPracticeMenu(room_code)
        return
    if _ammo_code == "arrows":
        $ player.remove_item("arrows_001", 1)
    elif _ammo_code == "droplets":
        $ player.remove_item("droplets_001", 1)
        $ player.remove_item("gunpowder_001", 1)
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = _ammo_code
    $ scene_runtime.text = "Вы спокойно заряжаете оружие {} для тренировки.".format(rusty_hunter_rifle_ammo_name(_ammo_code))
    $ scene_runtime.location_text = scene_runtime.text
    call ShootingPracticeMenu(room_code)
    return


label ShootingPracticeUnload(room_code=""):
    $ renpy.dynamic("_loaded_ammo")
    $ _loaded_ammo = rusty_hunter_rifle_loaded_ammo()
    if _loaded_ammo == "":
        $ scene_runtime.text = "Оружие и так уже разряжено."
        $ scene_runtime.location_text = scene_runtime.text
        call ShootingPracticeMenu(room_code)
        return
    if _loaded_ammo == "arrows":
        $ player.add_item("arrows_001", 1)
    elif _loaded_ammo == "droplets":
        $ player.add_item("droplets_001", 1)
        $ player.add_item("gunpowder_001", 1)
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = ""
    $ scene_runtime.text = "Вы снимаете заряд и снова оставляете оружие разряженным."
    $ scene_runtime.location_text = scene_runtime.text
    call ShootingPracticeMenu(room_code)
    return


label ShootingPracticeFire(room_code=""):
    $ renpy.dynamic("_loaded_ammo")
    $ _loaded_ammo = rusty_hunter_rifle_loaded_ammo()
    if _loaded_ammo == "":
        $ scene_runtime.text = "Сначала нужно зарядить оружие."
        $ scene_runtime.location_text = scene_runtime.text
        call ShootingPracticeMenu(room_code)
        return
    python:
        calendar_v2.advance_minutes(30)
        player.change_stat("fun", 3)
        player.change_stat("energy", -4)
    $ scene_runtime.text = shooting_practice_fire_text(_loaded_ammo, room_code)
    $ scene_runtime.location_text = scene_runtime.text
    $ rusty_hunter_rifle_item().state["loaded_ammo"] = ""
    call stat
    call ShootingPracticeMenu(room_code)
    return
