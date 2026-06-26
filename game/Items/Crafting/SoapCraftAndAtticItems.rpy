# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default SoapExpireDay = 0
default SoapAshBarrelInstalled = 0
default SoapAshBarrelReadyDay = 0
default SoapPendingBatches = []
default SoapStoredBatches = []
default SoapLookBonusUntilDay = -1
default SoapRequestQueue = {}
default HouseholdSoapSampleIntroDone = 0
default HouseholdSoapSampleGiven = {}
default HouseholdSoapLastBatchProfile = {}
default AtticLootFound = 0
default AtticSupplyLootFound = 0
default UpstairsRoomSearchState = {}
default RustyHunterRifleLoadedAmmo = ""

init 4 python:
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
        return ("recipe_book_001", "rusty_hunter_rifle_001", "old_leather_cuirass_001", "soap_001", "cork_001")

    def player_has_attic_manageable_items():
        for item_id in attic_manageable_item_ids():
            if _player_item_count_by_id(item_id) > 0:
                return True
        return False

    def attic_item_equipped_text(item_id):
        item_key = str(item_id or "").strip()
        if item_key == str(EquippedWeapon or ""):
            return "Сейчас это оружие у вас наготове."
        if item_key == str(EquippedArmor or ""):
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
        return str(RustyHunterRifleLoadedAmmo or "").strip()

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
        if item_id == str(EquippedWeapon or ""):
            return caption + " (оружие)"
        if item_id == str(EquippedArmor or ""):
            return caption + " (надето)"
        return caption

    def _soap_player_has_any(item_ids):
        for item_id in tuple(item_ids or ()):
            if _player_item_count_by_id(str(item_id or "").strip()) > 0:
                return True
        return False

    def soap_recipe_chain_discovered():
        return player_has_soap_recipe_book() or int(AtticLootFound or 0) == 1

    def player_has_soap_recipe_book():
        if _player_item_count_by_id("recipe_book_001") > 0:
            return True
        try:
            if _room_has_item_by_id(TavernMyRoomRoom, "recipe_book_001"):
                return True
        except Exception:
            pass
        try:
            if CurrentRoom is not None and _room_has_item_by_id(CurrentRoom, "recipe_book_001"):
                return True
        except Exception:
            pass
        return False

    def player_has_soap_bowl():
        return _soap_player_has_any(("night_bowl_001", "bucket_001"))

    def soap_selected_flower_item():
        if _player_item_count_by_id("lavender_001") > 0:
            return "lavender_001"
        if _player_item_count_by_id("wild_rose_001") > 0:
            return "wild_rose_001"
        return ""

    def soap_available_piece_count():
        return max(0, int(_player_item_count_by_id("soap_001") or 0))

    def soap_total_piece_count():
        return max(0, int(_player_item_count_by_id("soap_001") or 0)) + max(0, int(_player_item_count_by_id("luxury_soap_001") or 0))

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
        profile = dict(HouseholdSoapLastBatchProfile or {})
        return str(profile.get("label", "душистое домашнее") or "душистое домашнее")

    def soap_ash_barrel_is_ready():
        if int(SoapAshBarrelInstalled or 0) != 1:
            return False
        return int(dayspassed or 0) >= int(SoapAshBarrelReadyDay or 0)

    def player_has_rifle_loading_ammo(ammo_code=""):
        ammo_key = str(ammo_code or "").strip()
        if ammo_key == "arrows":
            return _player_item_count_by_id("arrows_001") > 0
        if ammo_key == "droplets":
            return _player_item_count_by_id("droplets_001") > 0 and _player_item_count_by_id("gunpowder_001") > 0
        return False

    def rusty_hunter_rifle_can_clean():
        return _player_item_count_by_id("rusty_hunter_rifle_001") > 0 and not rusty_hunter_rifle_is_cleaned()

    def rusty_hunter_rifle_can_oil():
        return (
            _player_item_count_by_id("rusty_hunter_rifle_001") > 0
            and rusty_hunter_rifle_is_cleaned()
            and not rusty_hunter_rifle_is_oiled()
            and _player_item_count_by_id("weapon_oil_001") > 0
        )

    def rusty_hunter_rifle_can_load(ammo_code=""):
        return (
            _player_item_count_by_id("rusty_hunter_rifle_001") > 0
            and rusty_hunter_rifle_is_cleaned()
            and rusty_hunter_rifle_is_oiled()
            and rusty_hunter_rifle_loaded_ammo() == ""
            and player_has_rifle_loading_ammo(ammo_code)
        )

    def rusty_hunter_rifle_can_unload():
        return _player_item_count_by_id("rusty_hunter_rifle_001") > 0 and rusty_hunter_rifle_loaded_ammo() != ""

    def player_can_train_shooting():
        if _player_item_count_by_id("rusty_hunter_rifle_001") <= 0:
            return False
        if not rusty_hunter_rifle_is_cleaned() or not rusty_hunter_rifle_is_oiled():
            return False
        if rusty_hunter_rifle_loaded_ammo() != "":
            return True
        return player_has_rifle_loading_ammo("arrows") or player_has_rifle_loading_ammo("droplets")

    def shooting_practice_intro_text(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        if room_key == "Backyard":
            return "Вы присматриваете безопасное место во дворе, ставите у стены старую доску и готовитесь проверить оружие на деле."
        return "Вы выбираете в лесу сухой пень и устраиваете короткую тренировку, чтобы почувствовать оружие в руках."

    def shooting_practice_fire_text(ammo_code="", room_code=""):
        ammo_key = str(ammo_code or "").strip()
        room_key = str(room_code or CurLoc or "").strip()
        if ammo_key == "droplets":
            if room_key == "Backyard":
                return "Вы даете короткий выстрел дробью по доске у стены. Грохот прокатывается по двору, а заряд выбивает из дерева облако щепок."
            return "Вы стреляете дробью по сухому пню. Заряд с треском разносит кору, а лес еще немного держит в воздухе эхо выстрела."
        if room_key == "Backyard":
            return "Вы выпускаете стрелу по самодельной мишени во дворе. Стрела уходит ровно, и вы лучше чувствуете, как работает старый механизм."
        return "Вы выпускаете стрелу в лесную мишень. Она с глухим стуком вонзается в древесину, и рука запоминает правильное усилие."

    def soap_can_cook_at_backyard():
        if str(CurLoc or "") != "Backyard":
            return False
        return recipe_page_can_craft("soap_recipe")

    def soap_can_cook_luxury_at_backyard():
        if str(CurLoc or "") != "Backyard":
            return False
        return recipe_page_can_craft("luxury_soap_recipe")

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
        appearance = player_state().appearance
        if not bool(allow_worn) and dress_name == str(appearance.current_dress or "").strip():
            return False
        if cloth_scrap_yield_for_dress(dress_name) <= 0:
            return False
        return appearance.has_dress(dress_name)

    def player_tear_wardrobe_dress(dress_code="", allow_worn=False, context_text=""):
        appearance = player_state().appearance
        dress_name = str(dress_code or "").strip()
        worn_now = dress_name == str(appearance.current_dress or "").strip()
        if worn_now and not bool(allow_worn):
            return {"ok": False, "text": "Сначала снимите одежду. Рвать можно только то, что уже лежит в ларе."}
        if not player_can_tear_wardrobe_dress(dress_name, allow_worn):
            return {"ok": False, "text": "Эту одежду сейчас нельзя пустить на лоскуты."}
        scrap_qty = cloth_scrap_yield_for_dress(dress_name)
        appearance.destroy_dress(dress_name)
        appearance.apply_to_store()
        _player_add_item_by_id("cloth_scrap_001", scrap_qty)
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
        current_dress = str(player_state().appearance.current_dress or "").strip()
        if current_dress == "":
            return {"ok": False, "text": "На вас уже нечему рваться."}
        return player_tear_wardrobe_dress(current_dress, True, context_text)

    def _soap_recipe_craft_handler(result_item_id="soap_001", use_olive_oil=False, recipe_id="soap_recipe"):
        global fun, SoapExpireDay, SoapAshBarrelReadyDay, HouseholdSoapLastBatchProfile

        item_result = str(result_item_id or "soap_001").strip()
        olive_required = bool(use_olive_oil)
        resolved_rows = recipe_page_requirement_status(recipe_id)
        soap_flower = recipe_resolved_item_id(resolved_rows, "flower_mix", soap_selected_flower_item())
        soap_flower_name = str(get_game_item(soap_flower).name if get_game_item(soap_flower) else "травы")
        soap_additives = [soap_flower]
        if _player_item_count_by_id("special_herbs_001") > 0:
            soap_additives.append("special_herbs_001")
        if _player_item_count_by_id("honey_comb_001") > 0:
            soap_additives.append("honey_comb_001")
        if olive_required:
            soap_additives.append("olive_oil_001")
        batch_profile = soap_batch_profile(soap_additives)
        consume_result = recipe_consume_required_ingredients(recipe_id, resolved_rows)
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять нужные вещи для мыла."), "recipe_id": recipe_id}
        if "special_herbs_001" in list(batch_profile.get("aroma_ids", ()) or ()):
            _player_remove_item_by_id("special_herbs_001", 1)
        if "honey_comb_001" in list(batch_profile.get("aroma_ids", ()) or ()):
            _player_remove_item_by_id("honey_comb_001", 1)
        fun = _player_clamp(fun + 20, 0, 100)
        calendar_v2.advance_minutes(120)
        HouseholdSoapLastBatchProfile = dict(batch_profile)
        SoapPendingBatches.append({
            "item_id": item_result,
            "quantity": 4,
            "ready_day": int(dayspassed or 0) + 7,
            "profile": dict(batch_profile),
        })
        SoapExpireDay = 0
        SoapAshBarrelReadyDay = int(dayspassed or 0) + 7
        update_stat_state()
        result_name = "роскошное мыло" if item_result == "luxury_soap_001" else "хозяйственное мыло"
        return {
            "ok": True,
            "text": "Вы разводите огонь во дворе, берете настоявшийся щелок из зольной бочки, кипятите его с {} и затем раскладываете густую массу по формам. Это будет {}; запах у партии выходит {}. Теперь мылу нужно как следует вылежаться: партия будет готова примерно через {{b}}неделю{{/b}}. В бочке уже поставлена новая зольная вода, и следующий щелок тоже настоится через неделю.".format(batch_profile.get("craft_text", soap_flower_name), result_name, batch_profile.get("label", soap_flower_name)),
            "recipe_id": recipe_id,
            "item_result": item_result,
            "quantity": 4,
        }

    def soap_recipe_craft_handler():
        return _soap_recipe_craft_handler("soap_001", False, "soap_recipe")

    def luxury_soap_recipe_craft_handler():
        return _soap_recipe_craft_handler("luxury_soap_001", True, "luxury_soap_recipe")

    def ethanol_recipe_craft_handler():
        consume_result = recipe_consume_required_ingredients("ethanol_recipe")
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять ингредиенты для спирта."), "recipe_id": "ethanol_recipe"}
        _player_add_item_by_id("ethanol_001", 1)
        calendar_v2.advance_minutes(90)
        update_stat_state()
        return {
            "ok": True,
            "text": "Вы давите ягоды, смешиваете их с медовой сладостью, даете настою дойти и затем аккуратно переливаете его в пустую бутылку. В итоге у вас получается бутылка крепкого спирта.",
            "recipe_id": "ethanol_recipe",
            "item_result": "ethanol_001",
            "quantity": 1,
        }

    def energy_tea_recipe_craft_handler():
        consume_result = recipe_consume_required_ingredients("energy_tea_recipe")
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять ингредиенты для чая."), "recipe_id": "energy_tea_recipe"}
        _player_add_item_by_id("energy_tea_001", 1)
        calendar_v2.advance_minutes(30)
        update_stat_state()
        return {
            "ok": True,
            "text": "Вы завариваете редкие травы с грибной щепотью и медовой сладостью. Настой выходит терпким, но бодрящим, и у вас получается порция бодрящего чая.",
            "recipe_id": "energy_tea_recipe",
            "item_result": "energy_tea_001",
            "quantity": 1,
        }

    def libido_recipe_selected_flavor_item():
        if _player_item_count_by_id("special_herbs_001") > 0:
            return "special_herbs_001"
        if _player_item_count_by_id("berries_001") > 0:
            return "berries_001"
        return ""

    def libido_recipe_craft_handler():
        consume_result = recipe_consume_required_ingredients("libido_recipe")
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять ингредиенты для настойки."), "recipe_id": "libido_recipe"}
        flavor_item = recipe_consumed_item_id(consume_result.get("consumed", []), "flavor_mix", libido_recipe_selected_flavor_item())
        if flavor_item == "":
            return {
                "ok": False,
                "text": "У вас нет ни редких трав, ни ягод, чтобы довести настой до ума.",
                "recipe_id": "libido_recipe",
            }
        _player_add_item_by_id("libido_tincture_001", 1)
        calendar_v2.advance_minutes(50)
        update_stat_state()
        flavor_name = "терпкие травы" if flavor_item == "special_herbs_001" else "раздавленные ягоды"
        return {
            "ok": True,
            "text": "Вы смешиваете крепкий спирт с медом и добавляете {}. Напиток получается куда мягче исходного настоя и хорошо годится для подарка, дружеской посиделки или продажи.".format(flavor_name),
            "recipe_id": "libido_recipe",
            "item_result": "libido_tincture_001",
            "quantity": 1,
        }

    def dry_moss_recipe_craft_handler():
        consume_result = recipe_consume_required_ingredients("dry_moss_recipe")
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять сырой мох."), "recipe_id": "dry_moss_recipe"}
        _player_add_item_by_id("dried_moss_001", 1)
        calendar_v2.advance_minutes(30)
        update_stat_state()
        return {
            "ok": True,
            "text": "Вы раскладываете сырой мох в сухом месте, даете ему как следует подсохнуть и перетираете его в сухую крошку. Получается заготовка для дальнейших смесей.",
            "recipe_id": "dry_moss_recipe",
            "item_result": "dried_moss_001",
            "quantity": 1,
        }

    def moss_gunpowder_recipe_craft_handler():
        consume_result = recipe_consume_required_ingredients("moss_gunpowder_recipe")
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять сушеный мох."), "recipe_id": "moss_gunpowder_recipe"}
        _player_add_item_by_id("gunpowder_001", 1)
        calendar_v2.advance_minutes(40)
        update_stat_state()
        return {
            "ok": True,
            "text": "Вы мелко перетираете высушенный мох и доводите смесь до плотного темного порошка. Получается самодельный пороховой заряд.",
            "recipe_id": "moss_gunpowder_recipe",
            "item_result": "gunpowder_001",
            "quantity": 1,
        }

    def healing_potion_recipe_craft_handler():
        consume_result = recipe_consume_required_ingredients("healing_potion_recipe")
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять ингредиенты для зелья."), "recipe_id": "healing_potion_recipe"}
        _player_add_item_by_id("healing_potion_001", 1)
        calendar_v2.advance_minutes(45)
        update_stat_state()
        return {
            "ok": True,
            "text": "Вы заливаете сушеный мох горячей водой, добавляете редкие травы и даете настою набрать силу. После этого аккуратно разливаете лечебный отвар по бутылке.",
            "recipe_id": "healing_potion_recipe",
            "item_result": "healing_potion_001",
            "quantity": 1,
        }

    def bandage_recipe_craft_handler():
        consume_result = recipe_consume_required_ingredients("bandage_recipe")
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять материалы для бинта."), "recipe_id": "bandage_recipe"}
        _player_add_item_by_id("bandage_001", 1)
        calendar_v2.advance_minutes(20)
        update_stat_state()
        return {
            "ok": True,
            "text": "Вы сворачиваете лоскут ткани с сухим мхом и получаете простой, но полезный перевязочный бинт.",
            "recipe_id": "bandage_recipe",
            "item_result": "bandage_001",
            "quantity": 1,
        }

    def cloth_rope_recipe_craft_handler():
        consume_result = recipe_consume_required_ingredients("cloth_rope_recipe")
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять лоскуты для веревки."), "recipe_id": "cloth_rope_recipe"}
        _player_add_item_by_id("rope_001", 1)
        calendar_v2.advance_minutes(40)
        update_stat_state()
        return {
            "ok": True,
            "text": "Вы долго скручиваете полосы ткани в плотный жгут, пока из них не выходит крепкая хозяйственная веревка.",
            "recipe_id": "cloth_rope_recipe",
            "item_result": "rope_001",
            "quantity": 1,
        }

    def fire_bomb_recipe_craft_handler():
        consume_result = recipe_consume_required_ingredients("fire_bomb_recipe")
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять ингредиенты для огненной бутылки."), "recipe_id": "fire_bomb_recipe"}
        _player_add_item_by_id("fire_bomb_001", 1)
        calendar_v2.advance_minutes(30)
        update_stat_state()
        return {
            "ok": True,
            "text": "Вы смешиваете масло со спиртом, добавляете сухой мох и плотно набиваете этим бутылку. Получается огненная бутылка, которую лучше держать подальше от открытого огня.",
            "recipe_id": "fire_bomb_recipe",
            "item_result": "fire_bomb_001",
            "quantity": 1,
        }

    def bat_repellent_recipe_craft_handler():
        consume_result = recipe_consume_required_ingredients("bat_repellent_recipe")
        if not bool(consume_result.get("ok", False)):
            return {"ok": False, "text": str(consume_result.get("text", "") or "Не удалось взять ингредиенты для дымной смеси."), "recipe_id": "bat_repellent_recipe"}
        _player_add_item_by_id("bat_repellent_001", 1)
        calendar_v2.advance_minutes(35)
        update_stat_state()
        return {
            "ok": True,
            "text": "Вы перетираете сушеный мох с лавандой и редкими травами, завариваете густую душную смесь и разливаете ее в бутылку. Получается едкий дымный состав, которым можно выкуривать дрянь из-под крыши.",
            "recipe_id": "bat_repellent_recipe",
            "item_result": "bat_repellent_001",
            "quantity": 1,
        }

    def player_can_use_soap():
        return _player_item_count_by_id("soap_001") > 0

    def soap_sync_batches():
        global SoapPendingBatches, SoapStoredBatches, SoapExpireDay

        if SoapPendingBatches is None:
            SoapPendingBatches = []
        elif not hasattr(SoapPendingBatches, "append"):
            SoapPendingBatches = list(SoapPendingBatches or [])
        if SoapStoredBatches is None:
            SoapStoredBatches = []
        elif not hasattr(SoapStoredBatches, "append"):
            SoapStoredBatches = list(SoapStoredBatches or [])

        current_day = int(dayspassed or 0)
        remaining_pending = []
        for batch in list(SoapPendingBatches or []):
            batch_data = dict(batch or {})
            quantity = max(0, int(batch_data.get("quantity", 0) or 0))
            ready_day = int(batch_data.get("ready_day", 0) or 0)
            profile = dict(batch_data.get("profile", {}) or {})
            item_id = str(batch_data.get("item_id", "") or "").strip()
            if item_id == "":
                item_id = "luxury_soap_001" if "olive_oil_001" in list(profile.get("aroma_ids", ()) or ()) else "soap_001"
            if quantity <= 0:
                continue
            if current_day >= ready_day:
                _player_add_item_by_id(item_id, quantity)
                SoapStoredBatches.append({
                    "item_id": item_id,
                    "quantity": quantity,
                    "ready_day": ready_day,
                    "profile": profile,
                })
            else:
                remaining_pending.append({
                    "item_id": item_id,
                    "quantity": quantity,
                    "ready_day": ready_day,
                    "profile": profile,
                })
        SoapPendingBatches = remaining_pending

        if len(list(SoapStoredBatches or [])) > 0:
            remaining_stored = []
            for batch in list(SoapStoredBatches or []):
                batch_data = dict(batch or {})
                quantity = max(0, int(batch_data.get("quantity", 0) or 0))
                if quantity <= 0:
                    continue
                profile = dict(batch_data.get("profile", {}) or {})
                item_id = str(batch_data.get("item_id", "") or "").strip()
                if item_id == "":
                    item_id = "luxury_soap_001" if "olive_oil_001" in list(profile.get("aroma_ids", ()) or ()) else "soap_001"
                remaining_stored.append({
                    "item_id": item_id,
                    "quantity": quantity,
                    "ready_day": int(batch_data.get("ready_day", current_day) or current_day),
                    "profile": profile,
                })
            SoapStoredBatches = remaining_stored
            SoapExpireDay = 0
            return

        SoapExpireDay = 0

    def soap_expire_if_needed():
        global SoapExpireDay

        soap_sync_batches()
        SoapExpireDay = 0

    def sync_soap_batches_with_day():
        soap_sync_batches()
        return int(_player_item_count_by_id("soap_001") or 0)

    def upstairs_room_search_done(room_code):
        room_key = str(room_code or "").strip()
        return int(dict(UpstairsRoomSearchState or {}).get(room_key, 0) or 0) > 0

    def upstairs_room_mark_searched(room_code):
        room_key = str(room_code or "").strip()
        UpstairsRoomSearchState[room_key] = 1

    def upstairs_room_search_text(room_code):
        room_key = str(room_code or "").strip()
        if upstairs_room_search_done(room_key):
            return "Вы уже осматривали эту комнату. Ничего нового в глаза не бросается."
        if room_key == "TavernAmandaRoom":
            return "Вы внимательнее осматриваете комнату Аманды. Под кроватью и возле ларей обнаруживается обычная девичья мелочь, а у ночного столика стоит ночная посудина."
        if room_key == "TavernSandraRoom":
            return "Вы осматриваете комнату Сандры. Здесь все сложено аккуратно, так что поиски не приносят ничего, кроме уважения к ее хозяйственности."
        if room_key == "TavernMelissaRoom":
            if int(effective_player_exploration() or 0) >= 100 and int(Melissa.var.get("bats_episode", 0) or 0) >= 2 and int(Melissa.var.get("bats_episode", 0) or 0) < 3:
                return "Вы осматриваете комнату Мелиссы внимательнее и замечаете под самым потолком несколько совсем маленьких щелей и норок в старом дереве. Оттуда тянет пылью и затхлым чердаком. Похоже, часть дряни лезет сюда не из самой комнаты, а сверху, через старую крышу и балки."
            if int(Melissa.var.get("bats_episode", 0) or 0) >= 3 and int(Melissa.var.get("bats_episode", 0) or 0) < 4:
                return "Теперь, когда вы знаете про щели под крышей, становится ясно: без осмотра чердака над комнатой Мелиссы эта история не закончится."
            if int(Melissa.var.get("bats_episode", 0) or 0) >= 4 and int(Melissa.var.get("bats_episode", 0) or 0) < 8:
                return "Вы еще раз осматриваете комнату Мелиссы и убеждаетесь, что без чистки чердака и заделки крыши мелкая дрянь будет возвращаться снова и снова."
            return "Вы осматриваете комнату Мелиссы. Ничего ценного не находится, зато становится ясно, что она старается держать свои пожитки в порядке."
        if room_key == "TavernEmptyRoom":
            return "Вы внимательно осматриваете пустую комнату. В углах только пыль, паутина и несколько забытых щепок."
        return "Вы осматриваете комнату, но не находите ничего важного."

    def amanda_night_bowl_available(_obj=None):
        return (
            str(CurLoc or "") == "TavernAmandaRoom"
            and int(time or 0) < 4
            and not amanda_has_given_night_bowl()
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
        name="мыло",
        description="Кусок домашнего мыла с легким травяным запахом.",
        price=4,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "crafted_good",
            "crafted_kind": "soap",
            "gift_value": 1,
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
            "crafted_kind": "luxury_soap",
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

    SoapRecipePage = RecipePage(
        recipe_id="soap_recipe",
        title="Хозяйственное мыло",
        image="images/recipe_book/soap_recipe.png",
        item_result="soap_001",
        ingredients={
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
            "pig_lard_001": {
                "quantity": 1,
                "unit": "кусок",
            },
            "flower_mix": {
                "quantity": 1,
                "unit": "пучок",
                "alternatives": ["lavender_001", "wild_rose_001"],
                "note": "Для запаха берут лаванду или дикую розу. Если под рукой есть редкие травы или мед, мастер пустит их в ту же партию.",
            },
        },
        unlocked=False,
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=4,
        notes=[
            "Варить мыло лучше во дворе, где есть огонь и место для большой посуды.",
            "Щелок готовится неделю, а сваренная партия вылеживается еще неделю.",
            "Оливковое масло лучше пустить в отдельную туалетную партию, а не в хозяйственное мыло.",
        ],
        craft_handler=soap_recipe_craft_handler,
    )
    register_recipe_page(SoapRecipePage)

    LuxurySoapRecipePage = RecipePage(
        recipe_id="luxury_soap_recipe",
        title="Туалетное мыло с оливковым маслом",
        image="images/recipe_book/soap_recipe.png",
        item_result="luxury_soap_001",
        ingredients={
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
            "pig_lard_001": {
                "quantity": 1,
                "unit": "кусок",
            },
            "flower_mix": {
                "quantity": 1,
                "unit": "пучок",
                "alternatives": ["lavender_001", "wild_rose_001"],
                "note": "Для запаха берут лаванду или дикую розу.",
            },
            "olive_oil_001": {
                "quantity": 1,
                "unit": "пузырек",
                "note": "Оливковое масло делает эту партию более мягкой и дорогой.",
            },
        },
        unlocked=False,
        unlock_condition=player_has_soap_recipe_book,
        result_quantity=4,
        notes=[
            "Это мыло годится для купания, ухода и подарков, а не только для хозяйственных нужд.",
            "Щелок готовится неделю, а сваренная партия вылеживается еще неделю.",
        ],
        craft_handler=luxury_soap_recipe_craft_handler,
    )
    register_recipe_page(LuxurySoapRecipePage)

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
        notes=[
            "Вощеная обмотка и крепкая палка позволяют сделать простой, но надежный факел.",
        ],
    )
    register_recipe_page(TorchRecipePage)

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
        notes=[
            "Сладкая ягодная брага дает крепкий настой, если с ней не торопиться.",
            "Готовый спирт лучше сразу перелить в пустую бутылку.",
        ],
        craft_handler=ethanol_recipe_craft_handler,
    )
    register_recipe_page(EthanolRecipePage)

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
        notes=[
            "Правильно заваренные травы и немного медовой сладости хорошо снимают усталость.",
        ],
        craft_handler=energy_tea_recipe_craft_handler,
    )
    register_recipe_page(EnergyTeaRecipePage)

    LibidoRecipePage = RecipePage(
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
        notes=[
            "Такая настойка уже годится не только для хозяйства, но и для дружеских разговоров.",
            "После пары глотков люди обычно становятся заметно разговорчивее и смелее.",
        ],
        craft_handler=libido_recipe_craft_handler,
    )
    register_recipe_page(LibidoRecipePage)

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
        unlock_condition=clara_paintings_special_cream_recipe_unlocked,
        result_quantity=1,
        notes=[
            "Серджио записал рецепт после того, как его отпустили по делу столичного жениха.",
            "Мазь годится для ухода, подарков и дальнейших интимных сцен, если они открыты сюжетом.",
        ],
    )
    register_recipe_page(SpecialCreamRecipePage)

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
        notes=[
            "Сырой мох сперва надо хорошо просушить, иначе он только испортит смесь.",
        ],
        craft_handler=dry_moss_recipe_craft_handler,
    )
    register_recipe_page(DryMossRecipePage)

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
        notes=[
            "Из хорошо высушенного мха выходит грубый, но годный порошок для старого охотничьего снаряжения.",
        ],
        craft_handler=moss_gunpowder_recipe_craft_handler,
    )
    register_recipe_page(MossGunpowderRecipePage)

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
        notes=[
            "Сушеный мох и редкие травы дают густой лечебный отвар, если заварить их в горячей воде.",
        ],
        craft_handler=healing_potion_recipe_craft_handler,
    )
    register_recipe_page(HealingPotionRecipePage)

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
        notes=[
            "Чистый лоскут и сухой мох дают простую, но полезную перевязку.",
        ],
        craft_handler=bandage_recipe_craft_handler,
    )
    register_recipe_page(BandageRecipePage)

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
        notes=[
            "Если ткани накопилось достаточно, ее можно пустить на грубую, но крепкую веревку.",
        ],
        craft_handler=cloth_rope_recipe_craft_handler,
    )
    register_recipe_page(ClothRopeRecipePage)

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
        notes=[
            "Это уже не хозяйственная поделка, а грубое зажигательное оружие.",
        ],
        craft_handler=fire_bomb_recipe_craft_handler,
    )
    register_recipe_page(FireBombRecipePage)

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
        unlock_condition=lambda: Melissa.bat_repellent_recipe_unlocked(),
        result_quantity=1,
        notes=[
            "Смесь годится не для лечения, а чтобы выкуривать из-под крыши мелкую дрянь и летучих тварей.",
        ],
        craft_handler=bat_repellent_recipe_craft_handler,
    )
    register_recipe_page(BatRepellentRecipePage)


label AtticInventoryMenu(return_context="attic", room_code="TavernAtic"):
    $ current_action_title = "Вещи"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _item_id in attic_manageable_item_ids():
            if _player_item_count_by_id(_item_id) > 0:
                current_action_items.append(MenuItem(attic_item_menu_caption(_item_id), Call("AtticInventoryItemMenu", _item_id, return_context, room_code)))
        if len(current_action_items) <= 0:
            MainTxt = "Сейчас у вас нет найденных на чердаке вещей при себе."
            CurLocDesc = MainTxt
        current_action_items.append(MenuItem("Назад", Call("AtticInventoryReturn", return_context, room_code)))
    return


label AtticInventoryItemMenu(item_id="", return_context="attic", room_code="TavernAtic", preserve_text=False):
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or _player_item_count_by_id(_item_id) <= 0:
        call AtticInventoryMenu(return_context, room_code)
        return
    $ _status_text = attic_item_equipped_text(_item_id)
    if not bool(preserve_text):
        if str(_status_text or "").strip() != "":
            $ MainTxt = runtime_item_description_text(_item_id) + "\n\n" + str(_status_text or "")
        else:
            $ MainTxt = runtime_item_description_text(_item_id)
        if _item_id == "rusty_hunter_rifle_001":
            $ MainTxt = str(MainTxt or "") + "\n\n" + "\n".join(rusty_hunter_rifle_status_lines())
        $ CurLocDesc = MainTxt
    $ current_action_title = runtime_item_display_name(_item_id) or str(_item_obj.name or "Вещь")
    $ current_action_content = None
    $ current_action_items = []
    if bool(getattr(_item_obj, "readable", False)):
        $ current_action_items.append(MenuItem("Прочитать", Call("AtticInventoryReadItem", _item_id, return_context, room_code)))
    if _item_id == "soap_001" and player_can_use_soap():
        $ current_action_items.append(MenuItem("Использовать мыло", Call("AtticInventoryUseSoap", _item_id, return_context, room_code)))
    if _item_id == "cork_001":
        $ current_action_items.append(MenuItem("Использовать пробку", Call("AtticInventoryUseCork", _item_id, return_context, room_code)))
    if _item_id == "rusty_hunter_rifle_001":
        if rusty_hunter_rifle_can_clean():
            $ current_action_items.append(MenuItem("Счистить ржавчину", Call("AtticInventoryRifleCleanRust", return_context, room_code)))
        if rusty_hunter_rifle_can_oil():
            $ current_action_items.append(MenuItem("Смазать механизм", Call("AtticInventoryRifleOil", return_context, room_code)))
        if rusty_hunter_rifle_can_load("arrows"):
            $ current_action_items.append(MenuItem("Зарядить стрелой", Call("AtticInventoryRifleLoadAmmo", "arrows", return_context, room_code)))
        if rusty_hunter_rifle_can_load("droplets"):
            $ current_action_items.append(MenuItem("Зарядить дробью", Call("AtticInventoryRifleLoadAmmo", "droplets", return_context, room_code)))
        if rusty_hunter_rifle_can_unload():
            $ current_action_items.append(MenuItem("Разрядить оружие", Call("AtticInventoryRifleUnload", return_context, room_code)))
    if str(_item_id) == str(EquippedWeapon or ""):
        $ current_action_items.append(MenuItem("Убрать оружие", Call("AtticInventoryUnequipItem", _item_id, return_context, room_code)))
    elif str(getattr(_item_obj, "custom_properties", {}).get("item_kind", "") or "") == "weapon":
        $ current_action_items.append(MenuItem("Вооружиться", Call("AtticInventoryEquipItem", _item_id, return_context, room_code)))
    if str(_item_id) == str(EquippedArmor or ""):
        $ current_action_items.append(MenuItem("Снять", Call("AtticInventoryUnequipItem", _item_id, return_context, room_code)))
    elif str(getattr(_item_obj, "custom_properties", {}).get("item_kind", "") or "") == "armor":
        $ current_action_items.append(MenuItem("Надеть", Call("AtticInventoryEquipItem", _item_id, return_context, room_code)))
    $ current_action_items.append(MenuItem("Оставить здесь", Call("AtticInventoryDropItem", _item_id, return_context, room_code)))
    $ current_action_items.append(MenuItem("Назад", Call("AtticInventoryMenu", return_context, room_code)))
    return


label AtticInventoryReadItem(item_id="", return_context="attic", room_code="TavernAtic"):
    $ _item_id = str(item_id or "").strip()
    if _item_id == "recipe_book_001":
        $ MainTxt = recipe_book_read_text()
        $ CurLocDesc = MainTxt
    call AtticInventoryItemMenu(_item_id, return_context, room_code, True)
    return


label AtticInventoryEquipItem(item_id="", return_context="attic", room_code="TavernAtic"):
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None or _player_item_count_by_id(_item_id) <= 0:
        call AtticInventoryMenu(return_context, room_code)
        return
    if str(getattr(_item_obj, "custom_properties", {}).get("item_kind", "") or "") == "weapon":
        $ EquippedWeapon = _item_id
        $ MainTxt = "Вы берете при себе " + runtime_item_display_name(_item_id) + "."
    elif str(getattr(_item_obj, "custom_properties", {}).get("item_kind", "") or "") == "armor":
        $ EquippedArmor = _item_id
        $ MainTxt = "Вы надеваете " + runtime_item_display_name(_item_id) + "."
    else:
        $ MainTxt = "Сейчас это нельзя надеть."
    $ CurLocDesc = MainTxt
    call stat
    call AtticInventoryItemMenu(_item_id, return_context, room_code, True)
    return


label AtticInventoryUnequipItem(item_id="", return_context="attic", room_code="TavernAtic"):
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_obj is None:
        call AtticInventoryMenu(return_context, room_code)
        return
    if _item_id == str(EquippedWeapon or ""):
        $ EquippedWeapon = ""
        $ MainTxt = "Вы убираете " + str(_item_obj.name or _item_id) + "."
    elif _item_id == str(EquippedArmor or ""):
        $ EquippedArmor = ""
        $ MainTxt = "Вы снимаете " + str(_item_obj.name or _item_id) + "."
    else:
        $ MainTxt = "Сейчас это и так не надето."
    $ CurLocDesc = MainTxt
    call stat
    call AtticInventoryItemMenu(_item_id, return_context, room_code, True)
    return


label AtticInventoryDropItem(item_id="", return_context="attic", room_code="TavernAtic"):
    $ _item_id = str(item_id or "").strip()
    $ _item_obj = get_game_item(_item_id)
    if _item_id == str(EquippedWeapon or ""):
        $ EquippedWeapon = ""
    if _item_id == str(EquippedArmor or ""):
        $ EquippedArmor = ""
    $ _drop_result = player_drop_item(CurrentRoom, _item_id)
    if _drop_result.get("ok", False):
        if _item_obj is not None:
            $ MainTxt = "Вы оставляете здесь " + str(_item_obj.name or _item_id) + "."
        else:
            $ MainTxt = str(_drop_result.get("text", "") or "Вы оставляете предмет здесь.")
    else:
        $ MainTxt = str(_drop_result.get("text", "") or "У вас этого нет.")
    $ CurLocDesc = MainTxt
    call stat
    call AtticInventoryMenu(return_context, room_code)
    return


label AtticInventoryUseSoap(item_id="", return_context="attic", room_code="TavernAtic"):
    if _player_item_count_by_id("soap_001") <= 0:
        $ MainTxt = "У вас больше не осталось мыла."
        $ CurLocDesc = MainTxt
        call AtticInventoryMenu(return_context, room_code)
        return
    $ _player_remove_item_by_id("soap_001", 1)
    $ player_state().appearance.wash()
    $ player_state().appearance.apply_to_store()
    $ SoapLookBonusUntilDay = int(dayspassed or 0) + 1
    $ fun = _player_clamp(fun + 2, 0, 100)
    call stat
    $ MainTxt = "Вы тщательно моетесь душистым домашним мылом. Кожа становится чище, запах приятнее, а выглядите вы заметно лучше. Чистота и свежесть еще какое-то время будут работать на ваш вид."
    if _player_item_count_by_id("soap_001") <= 0:
        $ MainTxt = MainTxt + "\n\nЭто был последний кусок обычного мыла."
    $ CurLocDesc = MainTxt
    call AtticInventoryMenu(return_context, room_code)
    return


label AtticInventoryUseCork(item_id="", return_context="attic", room_code="TavernAtic"):
    if int(_player_item_count_by_id("cork_001") or 0) <= 0:
        $ MainTxt = "У вас сейчас нет пробки."
        $ CurLocDesc = MainTxt
        call AtticInventoryMenu(return_context, room_code)
        return
    if int(_player_item_count_by_id("empty_bottle_001") or 0) <= 0 and int(_player_item_count_by_id("ethanol_001") or 0) <= 0:
        $ MainTxt = "Пробку пока не к чему применить. У вас нет под рукой подходящей бутылки."
        $ CurLocDesc = MainTxt
        call AtticInventoryMenu(return_context, room_code)
        return
    $ _player_remove_item_by_id("cork_001", 1)
    $ MainTxt = "Вы плотно затыкаете бутылку пробкой. Теперь содержимое не расплещется по дороге."
    $ CurLocDesc = MainTxt
    call AtticInventoryMenu(return_context, room_code)
    return


label AtticInventoryRifleCleanRust(return_context="attic", room_code="TavernAtic"):
    $ _rifle_item = rusty_hunter_rifle_item()
    if _rifle_item is None or _player_item_count_by_id("rusty_hunter_rifle_001") <= 0:
        call AtticInventoryMenu(return_context, room_code)
        return
    if rusty_hunter_rifle_is_cleaned():
        $ MainTxt = "Вы уже счистили основную ржавчину с механизма."
    else:
        $ _rifle_item.state["rust_cleaned"] = 1
        $ MainTxt = "Вы долго скоблите металл, снимаете рыжий налет и понемногу приводите механизм в порядок. Оружие уже не выглядит совсем уж мертвым."
    $ CurLocDesc = MainTxt
    call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
    return


label AtticInventoryRifleOil(return_context="attic", room_code="TavernAtic"):
    $ _rifle_item = rusty_hunter_rifle_item()
    if _rifle_item is None or _player_item_count_by_id("rusty_hunter_rifle_001") <= 0:
        call AtticInventoryMenu(return_context, room_code)
        return
    if not rusty_hunter_rifle_is_cleaned():
        $ MainTxt = "Сначала нужно счистить ржавчину, иначе толку от масла будет мало."
    elif rusty_hunter_rifle_is_oiled():
        $ MainTxt = "Механизм уже смазан и ходит заметно мягче."
    elif _player_item_count_by_id("weapon_oil_001") <= 0:
        $ MainTxt = "У вас нет оружейного масла."
    else:
        $ _player_remove_item_by_id("weapon_oil_001", 1)
        $ _rifle_item.state["oiled"] = 1
        $ MainTxt = "Вы аккуратно смазываете механизм оружейным маслом. Скрип уходит, а детали начинают двигаться куда увереннее."
    $ CurLocDesc = MainTxt
    call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
    return


label AtticInventoryRifleLoadAmmo(ammo_code="arrows", return_context="attic", room_code="TavernAtic"):
    $ _ammo_code = str(ammo_code or "").strip()
    if not rusty_hunter_rifle_can_load(_ammo_code):
        $ MainTxt = "Сейчас оружие нельзя так зарядить."
        $ CurLocDesc = MainTxt
        call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
        return
    if _ammo_code == "arrows":
        $ _player_remove_item_by_id("arrows_001", 1)
    elif _ammo_code == "droplets":
        $ _player_remove_item_by_id("droplets_001", 1)
        $ _player_remove_item_by_id("gunpowder_001", 1)
    $ RustyHunterRifleLoadedAmmo = _ammo_code
    $ MainTxt = "Вы заряжаете оружие {} и осторожно ставите механизм наготове.".format(rusty_hunter_rifle_ammo_name(_ammo_code))
    $ CurLocDesc = MainTxt
    call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
    return


label AtticInventoryRifleUnload(return_context="attic", room_code="TavernAtic"):
    $ _loaded_ammo = rusty_hunter_rifle_loaded_ammo()
    if _loaded_ammo == "":
        $ MainTxt = "Оружие и так уже разряжено."
        $ CurLocDesc = MainTxt
        call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
        return
    if _loaded_ammo == "arrows":
        $ _player_add_item_by_id("arrows_001", 1)
    elif _loaded_ammo == "droplets":
        $ _player_add_item_by_id("droplets_001", 1)
        $ _player_add_item_by_id("gunpowder_001", 1)
    $ RustyHunterRifleLoadedAmmo = ""
    $ MainTxt = "Вы осторожно разряжаете оружие и убираете заряд."
    $ CurLocDesc = MainTxt
    call AtticInventoryItemMenu("rusty_hunter_rifle_001", return_context, room_code, True)
    return


label AtticInventoryReturn(return_context="attic", room_code="TavernAtic"):
    if str(return_context or "") == "chest":
        call TavernMyRoomOpenChest
        return
    if str(room_code or "") == "TavernAtic":
        call TavernAticRestore
        return
    jump expression room_code


label UpstairsRoomSearch(room_code="", restore_label=""):
    $ _up_room_code = str(room_code or CurLoc or "")
    $ findAvailableEvents(True)
    if story_event_available(_up_room_code, "room_search"):
        call checkTriggers(_up_room_code, "room_search", 0)
        return
    $ MainTxt = upstairs_room_search_text(_up_room_code)
    $ CurLocDesc = MainTxt
    if str(_up_room_code or "") == "TavernMelissaRoom" and int(effective_player_exploration() or 0) >= 100 and int(Melissa.var.get("bats_episode", 0) or 0) >= 2 and int(Melissa.var.get("bats_episode", 0) or 0) < 3:
        $ Melissa.var["bats_episode"] = 3
    $ upstairs_room_mark_searched(_up_room_code)
    if str(restore_label or "") != "" and renpy.has_label(str(restore_label or "")):
        call expression str(restore_label or "")
        return
    jump expression _up_room_code


label BackyardCookSoap(recipe_id="soap_recipe"):
    $ _soap_recipe_id = str(recipe_id or "soap_recipe").strip()
    if not recipe_page_can_craft(_soap_recipe_id):
        $ MainTxt = "У вас нет необходимых ингредиентов, чтобы сварить мыло."
        $ CurLocDesc = MainTxt
        call BackyardObjectMenu("backyard_ash_barrel", True)
        return

    $ _soap_craft_result = apply_recipe_craft(_soap_recipe_id)
    $ MainTxt = str(_soap_craft_result.get("text", "") or "Вы варите мыло.")
    $ CurLocDesc = MainTxt
    call BackyardObjectMenu("backyard_ash_barrel", True)
    return


label ShootingPracticeMenu(room_code=""):
    $ _shoot_room_code = str(room_code or CurLoc or "").strip()
    if not player_can_train_shooting():
        $ MainTxt = "Сейчас вам нечем как следует потренироваться в стрельбе."
        $ CurLocDesc = MainTxt
        call ShootingPracticeReturn(_shoot_room_code)
        return
    $ MainTxt = shooting_practice_intro_text(_shoot_room_code)
    $ CurLocDesc = MainTxt
    $ current_action_title = "Стрельба"
    $ current_action_content = None
    $ current_action_items = []
    if rusty_hunter_rifle_loaded_ammo() != "":
        $ current_action_items.append(MenuItem("Сделать пробный выстрел ({})".format(rusty_hunter_rifle_ammo_name(rusty_hunter_rifle_loaded_ammo())), Call("ShootingPracticeFire", _shoot_room_code)))
    if rusty_hunter_rifle_can_load("arrows"):
        $ current_action_items.append(MenuItem("Зарядить стрелой", Call("ShootingPracticeLoadAmmo", "arrows", _shoot_room_code)))
    if rusty_hunter_rifle_can_load("droplets"):
        $ current_action_items.append(MenuItem("Зарядить дробью", Call("ShootingPracticeLoadAmmo", "droplets", _shoot_room_code)))
    if rusty_hunter_rifle_can_unload():
        $ current_action_items.append(MenuItem("Разрядить оружие", Call("ShootingPracticeUnload", _shoot_room_code)))
    $ current_action_items.append(MenuItem("Назад", Call("ShootingPracticeReturn", _shoot_room_code)))
    return


label ShootingPracticeLoadAmmo(ammo_code="arrows", room_code=""):
    $ _ammo_code = str(ammo_code or "").strip()
    if not rusty_hunter_rifle_can_load(_ammo_code):
        $ MainTxt = "Сейчас оружие нельзя так зарядить."
        $ CurLocDesc = MainTxt
        call ShootingPracticeMenu(room_code)
        return
    if _ammo_code == "arrows":
        $ _player_remove_item_by_id("arrows_001", 1)
    elif _ammo_code == "droplets":
        $ _player_remove_item_by_id("droplets_001", 1)
        $ _player_remove_item_by_id("gunpowder_001", 1)
    $ RustyHunterRifleLoadedAmmo = _ammo_code
    $ MainTxt = "Вы спокойно заряжаете оружие {} для тренировки.".format(rusty_hunter_rifle_ammo_name(_ammo_code))
    $ CurLocDesc = MainTxt
    call ShootingPracticeMenu(room_code)
    return


label ShootingPracticeUnload(room_code=""):
    $ _loaded_ammo = rusty_hunter_rifle_loaded_ammo()
    if _loaded_ammo == "":
        $ MainTxt = "Оружие и так уже разряжено."
        $ CurLocDesc = MainTxt
        call ShootingPracticeMenu(room_code)
        return
    if _loaded_ammo == "arrows":
        $ _player_add_item_by_id("arrows_001", 1)
    elif _loaded_ammo == "droplets":
        $ _player_add_item_by_id("droplets_001", 1)
        $ _player_add_item_by_id("gunpowder_001", 1)
    $ RustyHunterRifleLoadedAmmo = ""
    $ MainTxt = "Вы снимаете заряд и снова оставляете оружие разряженным."
    $ CurLocDesc = MainTxt
    call ShootingPracticeMenu(room_code)
    return


label ShootingPracticeFire(room_code=""):
    $ _loaded_ammo = rusty_hunter_rifle_loaded_ammo()
    if _loaded_ammo == "":
        $ MainTxt = "Сначала нужно зарядить оружие."
        $ CurLocDesc = MainTxt
        call ShootingPracticeMenu(room_code)
        return
    python:
        global fun, energy
        calendar_v2.advance_minutes(30)
        fun = _player_clamp(fun + 3, 0, 100)
        energy = _player_clamp(energy - 4, 0, 100)
    $ MainTxt = shooting_practice_fire_text(_loaded_ammo, room_code)
    $ CurLocDesc = MainTxt
    $ RustyHunterRifleLoadedAmmo = ""
    call stat
    call ShootingPracticeMenu(room_code)
    return


label ShootingPracticeReturn(room_code=""):
    $ _shoot_room_code = str(room_code or CurLoc or "").strip()
    if _shoot_room_code == "Backyard":
        call BackyardRestore
        return
    if _shoot_room_code == "Forest":
        call ForestRestore
        return
    if room_in_group(_shoot_room_code, ROOM_GROUP_FOREST):
        call ForestSubroomRestore
        return
    jump expression _shoot_room_code


label UseEnergyTeaItem:
    call UseDrinkItem("energy_tea_001")
    return


label UseLibidoTinctureItem:
    call UseDrinkItem("libido_tincture_001")
    return
