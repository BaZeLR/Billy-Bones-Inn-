default action_override_text = ""

init -46 python:

    def _player_clamp(value, low, high):
        return max(low, min(high, int(value or 0)))

    def _ensure_player_inventory_store():
        global playerItems

        if isinstance(playerItems, dict):
            normalized = {}
            for raw_key, raw_count in list(playerItems.items()):
                item_key = get_object_id(raw_key)
                if not item_key:
                    continue
                try:
                    item_count = int(raw_count or 0)
                except Exception:
                    item_count = 0
                if item_count > 0:
                    normalized[item_key] = normalized.get(item_key, 0) + item_count
            playerItems = normalized
            return playerItems

        normalized = {}
        for raw_item in list(playerItems or []):
            item_key = get_object_id(raw_item)
            if not item_key:
                continue
            normalized[item_key] = normalized.get(item_key, 0) + 1
        playerItems = normalized
        return playerItems

    def _player_item_count_by_id(item_id):
        inventory = _ensure_player_inventory_store()
        item_key = get_object_id(item_id)
        if not item_key:
            return 0
        return max(0, int(inventory.get(item_key, 0) or 0))

    def _player_inventory_item_ids(expand_stacks=False):
        inventory = _ensure_player_inventory_store()
        item_ids = []
        for item_key in sorted(list(inventory.keys())):
            item_count = max(0, int(inventory.get(item_key, 0) or 0))
            if item_count <= 0:
                continue
            if expand_stacks:
                for _unused_item_unit in range(item_count):
                    item_ids.append(item_key)
            else:
                item_ids.append(item_key)
        return item_ids

    def _room_remove_item_by_id(room_obj, item_id):
        if room_obj is None or not hasattr(room_obj, "game_items"):
            return False

        item_id = get_object_id(item_id)
        if not item_id:
            return False

        updated_items = []
        removed = False
        for row in list(room_obj.game_items or []):
            row_id = get_object_id(row)

            if not removed and row_id == item_id:
                removed = True
                continue

            updated_items.append(row)

        if removed:
            room_obj.game_items = updated_items
            room_obj.objects = room_obj.game_items

        return removed

    def _room_add_item_by_id(room_obj, item_id):
        if room_obj is None or not hasattr(room_obj, "game_items"):
            return False

        item_id = get_object_id(item_id)
        if not item_id:
            return False

        room_obj.game_items.append(item_id)
        room_obj.objects = room_obj.game_items
        return True

    def _room_item_count_by_id(room_obj, item_id):
        if room_obj is None or not hasattr(room_obj, "game_items"):
            return 0

        item_id = get_object_id(item_id)
        if not item_id:
            return 0

        total = 0
        for row in list(room_obj.game_items or []):
            if get_object_id(row) == item_id:
                total += 1
        return total

    def _room_has_item_by_id(room_obj, item_id):
        return _room_item_count_by_id(room_obj, item_id) > 0

    def _player_can_sleep_now():
        try:
            calendar_sync_state()
        except Exception:
            pass

        try:
            current_slot = int(time or 0)
        except Exception:
            current_slot = 0

        try:
            current_hour = int(hour or 0)
        except Exception:
            current_hour = 0

        return current_slot >= 4 or current_hour >= 23

    def _room_add_item_units(room_obj, item_id, units=1):
        added = False
        total_units = max(0, int(units or 0))
        for _unused_room_unit in range(total_units):
            if _room_add_item_by_id(room_obj, item_id):
                added = True
        return added

    def _object_state_int(game_object, state_key, default=0):
        if game_object is None or not hasattr(game_object, "state"):
            return int(default or 0)
        try:
            return int(game_object.state.get(str(state_key or ""), default) or default)
        except Exception:
            return int(default or 0)

    def _set_object_state_int(game_object, state_key, value):
        if game_object is None:
            return 0
        if not hasattr(game_object, "state") or not isinstance(game_object.state, dict):
            game_object.state = {}
        game_object.state[str(state_key or "")] = int(value or 0)
        return int(game_object.state[str(state_key or "")])

    def _add_object_state_int(game_object, state_key, delta, minimum=0):
        current_value = _object_state_int(game_object, state_key, 0)
        next_value = max(int(minimum or 0), current_value + int(delta or 0))
        return _set_object_state_int(game_object, state_key, next_value)

    def _player_remove_item_by_id(item_id, quantity=1):
        item_id = get_object_id(item_id)
        if not item_id:
            return False

        inventory = _ensure_player_inventory_store()
        current_count = max(0, int(inventory.get(item_id, 0) or 0))
        remove_count = max(1, int(quantity or 1))
        if current_count < remove_count:
            return False

        if current_count == remove_count:
            if item_id in inventory:
                del inventory[item_id]
        else:
            inventory[item_id] = current_count - remove_count

        return True

    def _player_add_item_by_id(item_id, quantity=1):
        item_id = get_object_id(item_id)
        if not item_id:
            return False

        inventory = _ensure_player_inventory_store()
        add_count = max(1, int(quantity or 1))
        inventory[item_id] = max(0, int(inventory.get(item_id, 0) or 0)) + add_count
        return True

    def _player_has_item_by_id(item_id):
        return _player_item_count_by_id(item_id) > 0

    def _action_display_name(char_name):
        key = str(char_name or "").strip()
        if not key:
            return ""
        try:
            return str(RealName.get(key, key) or key)
        except Exception:
            return key

    def _action_sync_openness(char_name):
        key = str(char_name or "").strip()
        if not key:
            return
        try:
            adjust_otkroven(key)
        except Exception:
            pass

    def take(room_obj, item_id):
        item_id = get_object_id(item_id)
        if not item_id:
            return {
                "ok": False,
                "text": "Нечего брать.",
                "action_key": "take",
                "item_id": item_id,
            }

        removed = _room_remove_item_by_id(room_obj, item_id)
        if not removed:
            return {
                "ok": False,
                "text": "Здесь уже нечего брать.",
                "action_key": "take",
                "item_id": item_id,
            }

        _player_add_item_by_id(item_id)
        game_item = get_game_item(item_id, room_obj)
        take_text = "Вы берете {}.".format(str(game_item.name).strip())

        return {
            "ok": True,
            "text": take_text,
            "action_key": "take",
            "item_id": item_id,
        }

    def player_pick_up_item(room_obj, item_id):
        result = take(room_obj, item_id)
        result["action_key"] = "pick_up"
        return result

    def player_drop_item(room_obj, item_id):
        item_key = str(item_id or "").strip()
        if not item_key:
            return {
                "ok": False,
                "text": "Нечего бросать.",
                "action_key": "drop",
                "item_id": item_key,
            }

        removed = _player_remove_item_by_id(item_key)
        if not removed:
            return {
                "ok": False,
                "text": "У вас этого нет.",
                "action_key": "drop",
                "item_id": item_key,
            }

        added = _room_add_item_by_id(room_obj, item_key)
        if not added:
            _player_add_item_by_id(item_key)
            return {
                "ok": False,
                "text": "Некуда положить предмет.",
                "action_key": "drop",
                "item_id": item_key,
            }

        return {
            "ok": True,
            "text": "Вы оставляете предмет здесь.",
            "action_key": "drop",
            "item_id": item_key,
        }

    def player_drink_item(item_id):
        global energy, fun

        item_key = str(item_id or "").strip()
        if not item_key:
            return {
                "ok": False,
                "text": "Пить нечего.",
                "action_key": "drink",
                "item_id": item_key,
            }

        if item_key == "drink_ale_001":
            minutes_cost = 30
            energy_gain = 10
            fun_gain = 5
            result_text = "Кружка доброго эля помогает немного расслабиться."
            item_name = "эль"
        elif item_key == "libido_tincture_001":
            minutes_cost = 40
            energy_gain = 8
            fun_gain = 8
            result_text = "Пряная настойка мягко ударяет в голову, разогревает кровь и заметно развязывает язык."
            item_name = "пряная настойка"
        else:
            return {
                "ok": False,
                "text": "Сейчас это нельзя выпить.",
                "action_key": "drink",
                "item_id": item_key,
            }

        calendar_advance_minutes(minutes_cost)
        update_stat_state()
        energy = _player_clamp(energy + energy_gain, 0, 100)
        fun = _player_clamp(fun + fun_gain, 0, 100)

        return {
            "ok": True,
            "text": result_text,
            "action_key": "drink",
            "item_id": item_key,
            "item_name": item_name,
        }

    def player_apply_item_social_effects(char_name="", item_id="", from_gift=False):
        global fun

        key = str(char_name or "").strip()
        item_key = str(item_id or "").strip()
        item_obj = get_game_item(item_key)
        if key == "" or item_obj is None:
            return {"text": "", "friend_bonus": 0, "openness_bonus": 0, "trust_bonus": 0, "horny_bonus": 0}

        custom_props = dict(getattr(item_obj, "custom_properties", {}) or {})
        fun_bonus = max(0, int(custom_props.get("social_fun_bonus", 0) or 0))
        openness_bonus = max(0, int(custom_props.get("social_openness_bonus", 0) or 0))
        trust_bonus = max(0, int(custom_props.get("social_trust_bonus", 0) or 0))
        horny_bonus = max(0, int(custom_props.get("social_horny_bonus", 0) or 0))
        friend_bonus = max(0, int(custom_props.get("social_friend_bonus", 0) or 0))

        if from_gift:
            if friend_bonus > 0:
                Friends[key] = max(0, min(20, int(Friends.get(key, 0) or 0) + friend_bonus))
            if fun_bonus > 0:
                fun = _player_clamp(fun + fun_bonus, 0, 100)
            if openness_bonus > 0 and isinstance(otkroven, dict):
                otkroven[key] = max(0, min(20, int(otkroven.get(key, 0) or 0) + openness_bonus))
            if trust_bonus > 0 and key == "clara" and isinstance(ClaraVar, dict):
                ClaraVar["trust"] = max(0, min(20, int(ClaraVar.get("trust", 0) or 0) + trust_bonus))
            if horny_bonus > 0 and isinstance(sluttiness, dict) and key in sluttiness:
                sluttiness[key] = max(0, min(100, int(sluttiness.get(key, 0) or 0) + horny_bonus))

            if item_key == "soap_001" and key in ("sandra", "melissa", "amanda"):
                if isinstance(beauty, dict):
                    beauty[key] = max(0, min(100, int(beauty.get(key, 0) or 0) + 20))
                Friends[key] = max(0, min(20, int(Friends.get(key, 0) or 0) + 3))
                if isinstance(sluttiness, dict):
                    sluttiness[key] = max(0, min(100, int(sluttiness.get(key, 0) or 0) + 2))
                if isinstance(neshlush, dict):
                    neshlush[key] = max(0, int(neshlush.get(key, 0) or 0) - 2)
                if int(Friends.get(key, 0) or 0) >= 7:
                    if not isinstance(SoapRequestQueue, dict):
                        globals()["SoapRequestQueue"] = {}
                    SoapRequestQueue[key] = 1
            elif item_key in ("berries_001", "mushroom_001", "honey_comb_001", "boar_meat_001") and key == "sandra":
                Friends[key] = max(0, min(20, int(Friends.get(key, 0) or 0) + 1))
                if fun_bonus <= 0:
                    fun = _player_clamp(fun + 1, 0, 100)

        effect_lines = []
        if fun_bonus > 0:
            effect_lines.append("{} заметно расслабляется и охотнее поддерживает разговор.".format(_action_display_name(key)))
        if openness_bonus > 0:
            effect_lines.append("{} делится чем-то более личным и говорит куда откровеннее обычного.".format(_action_display_name(key)))
        if trust_bonus > 0 and key == "clara":
            effect_lines.append("Похоже, Кларисса начинает доверять вам заметно больше.")
        if horny_bonus > 0:
            effect_lines.append("От подарка в ее глазах появляется теплый, немного шальной блеск.")
        if item_key == "soap_001" and key in ("sandra", "melissa", "amanda"):
            effect_lines.append("{} сразу заметно хорошеет, становится мягче и послушнее, а чистый запах явно поднимает ей настроение.".format(_action_display_name(key)))
            if int(Friends.get(key, 0) or 0) >= 7:
                effect_lines.append("Похоже, ей так нравится это мыло, что потом она наверняка попросит у вас еще.")
        if item_key in ("berries_001", "mushroom_001", "honey_comb_001") and key == "sandra":
            effect_lines.append("Сандра сразу прикидывает, как пустить это в дело на кухне, и обещает сварить что-нибудь вкусное для всей трактирной челяди.")
        if item_key == "boar_meat_001" and key == "sandra":
            effect_lines.append("Сандра деловито прикидывает, как лучше разделать мясо, и обещает пустить его на сытный общий стол для домочадцев.")
        if item_key == "drink_ale_001" and key == "amanda":
            effect_lines.append("Аманда быстро веселееет, смеется куда громче обычного и явно рада, что вы решили разделить с ней выпивку.")
        if item_key == "drink_ale_001" and key == "melissa":
            effect_lines.append("Мелисса отпивает эль осторожно, но вскоре заметно расслабляется и начинает отвечать вам теплее.")
        if item_key == "energy_tea_001" and key == "sandra":
            effect_lines.append("Сандра одобрительно кивает: хороший чай явно пришелся кстати среди бесконечных трактирных хлопот.")
        if item_key == "energy_tea_001" and key == "melissa":
            effect_lines.append("Мелисса благодарит вас за горячий чай и после него охотнее задерживается рядом, не спеша уходить по делам.")
        if item_key == "libido_tincture_001" and key == "clara":
            effect_lines.append("Кларисса чуть дольше задерживает на вас взгляд и отвечает заметно более игривым тоном.")
        if item_key == "soap_001" and key == "sandra":
            effect_lines.append("Сандра сразу начинает прикидывать, как такое мыло оценят в трактире, и явно довольна тем, что вы подумали о хозяйстве.")
        if item_key == "soap_001" and key == "melissa":
            effect_lines.append("Мелисса почти смущенно улыбается, оценив и сам подарок, и то, что вы заметили ее заботу о себе.")
        if item_key == "soap_001" and key == "amanda":
            effect_lines.append("Аманда принимает мыло с живым интересом и тут же начинает болтать, как приятно будет пахнуть после него.")

        return {
            "text": " ".join(effect_lines).strip(),
            "friend_bonus": friend_bonus,
            "openness_bonus": openness_bonus,
            "trust_bonus": trust_bonus,
            "horny_bonus": horny_bonus,
        }

    def player_share_item_with(char_name="", item_id=""):
        global fun

        key = str(char_name or "").strip()
        item_key = str(item_id or "").strip()
        item_obj = get_game_item(item_key)
        if key == "" or item_obj is None:
            return {"ok": False, "text": "Сейчас этим нельзя ни с кем поделиться.", "action_key": "share"}

        custom_props = dict(getattr(item_obj, "custom_properties", {}) or {})
        item_kind = str(custom_props.get("item_kind", "") or "").strip()
        loot_kind = str(custom_props.get("loot_kind", "") or "").strip()
        if item_kind not in ("drink", "forest_resource", "crafted_good", "ingredient") and not (item_kind == "animal_loot" and loot_kind == "meat"):
            return {"ok": False, "text": "Сейчас этим делиться не очень уместно.", "action_key": "share"}

        removed = _player_remove_item_by_id(item_key, 1)
        if not removed:
            return {"ok": False, "text": "Этой вещи у вас больше нет.", "action_key": "share"}

        Talked[key] = int(Talked.get(key, 0) or 0) + 1
        GiftedToday[key] = int(GiftedToday.get(key, 0) or 0) + 1
        TalkedToday[key] = int(TalkedToday.get(key, 0) or 0) + 1
        _action_sync_openness(key)

        if item_key == "drink_ale_001":
            _player_add_item_by_id("empty_bottle_001", 1)
            _player_add_item_by_id("cork_001", 1)

        base_friend = max(1, int(custom_props.get("gift_value", 1) or 1))
        Friends[key] = max(0, min(20, int(Friends.get(key, 0) or 0) + base_friend))
        fun = _player_clamp(fun + max(1, int(custom_props.get("social_fun_bonus", 0) or 0)), 0, 100)
        effect_result = player_apply_item_social_effects(key, item_key, True)

        share_text = "{} принимает угощение и вы проводите вместе несколько спокойных минут.".format(_action_display_name(key))
        if item_key == "drink_ale_001":
            share_text = "Вы откупориваете бутылку эля и делите ее с {}. Разговор быстро становится проще и веселее.".format(_action_display_name(key))
        elif item_key == "energy_tea_001":
            share_text = "Вы завариваете бодрящий чай для {}. Горячий напиток помогает перевести дух и разговориться.".format(_action_display_name(key))
        elif item_key == "libido_tincture_001":
            share_text = "Вы делитесь пряной настойкой с {}. Напиток приятно разогревает кровь и быстро делает разговор откровеннее.".format(_action_display_name(key))
        elif item_key in ("berries_001", "mushroom_001", "honey_comb_001") and key == "sandra":
            share_text = "Вы отдаете {} {}. Сандра сразу думает, как пустить находку в дело и обещает приготовить для всей трактирной челяди что-нибудь вкусное.".format(_action_display_name(key), getattr(item_obj, "name", item_key))
        elif item_key == "boar_meat_001" and key == "sandra":
            share_text = "Вы приносите {} свежего кабаньего мяса. Сандра тут же прикидывает, что из него выйдет сытный стол для домочадцев, и явно довольна такой добычей.".format(_action_display_name(key))

        if item_key == "drink_ale_001" and key in ("melissa", "amanda"):
            if isinstance(sluttiness, dict):
                sluttiness[key] = max(0, min(100, int(sluttiness.get(key, 0) or 0) + 1))

        result_text = share_text
        if str(effect_result.get("text", "") or "").strip():
            result_text += " " + str(effect_result.get("text", "") or "").strip()

        return {
            "ok": True,
            "text": result_text,
            "action_key": "share",
            "char_name": key,
            "item_id": item_key,
        }

    def player_eat_meal(item_name, item_energy):
        global energy, fun

        item_label = str(item_name or "еду").strip() or "еду"
        energy_gain = max(0, int(item_energy or 0))

        calendar_advance_minutes(30)
        update_stat_state()
        energy = _player_clamp(energy + energy_gain, 0, 100)
        fun = _player_clamp(fun + 5, 0, 100)

        return {
            "ok": True,
            "text": "Вы съедаете {} и чувствуете, как силы понемногу возвращаются.".format(item_label),
            "action_key": "eat",
            "item_name": item_label,
            "item_energy": energy_gain,
        }

    def player_wash_with_rainwater():
        global dayssincewash, energy

        calendar_advance_minutes(30)
        dayssincewash = 0
        update_stat_state()
        energy = _player_clamp(energy - 5, 0, 100)

        return {
            "ok": True,
            "text": "Вы умываетесь и наскоро обмываетесь холодной дождевой водой. Это освежает и помогает привести себя в порядок.",
            "action_key": "wash",
        }

    def player_talk_to(char_name):
        global fun

        key = str(char_name or "").strip()
        if not key:
            return {"ok": False, "text": "Не с кем разговаривать.", "action_key": "talk"}

        calendar_advance_minutes(30)
        update_stat_state()

        Talked[key] = int(Talked.get(key, 0) or 0) + 1
        current_friend = int(Friends.get(key, 0) or 0)
        friend_gain = resolve_player_social_delta(key, "talk")
        if friend_gain != 0:
            Friends[key] = max(0, min(20, current_friend + friend_gain))
        _action_sync_openness(key)
        TalkedToday[key] = int(TalkedToday.get(key, 0) or 0) + 1

        fun = _player_clamp(fun + 2, 0, 100)
        if friend_gain > 0:
            result_text = "Вы некоторое время беседуете с {}. Разговор проходит заметно теплее обычного.".format(_action_display_name(key))
        elif friend_gain < 0:
            result_text = "Вы пытаетесь побеседовать с {}, но разговор выходит не слишком удачным.".format(_action_display_name(key))
        else:
            result_text = "Вы некоторое время беседуете с {}.".format(_action_display_name(key))

        return {
            "ok": True,
            "text": result_text,
            "action_key": "talk",
            "char_name": key,
            "friend_delta": friend_gain,
        }

    def player_gift_to(char_name, gift_name="подарок", friend_gain=2, gift_item_id=""):
        key = str(char_name or "").strip()
        gift = str(gift_name or "подарок").strip()
        gift_item = str(gift_item_id or "").strip()
        gain = int(friend_gain or 2)
        if not key:
            return {"ok": False, "text": "Некому дарить подарок.", "action_key": "gift"}

        gain = resolve_player_social_delta(key, "gift", gain, gift_item)
        Friends[key] = max(0, min(20, int(Friends.get(key, 0) or 0) + gain))
        Talked[key] = int(Talked.get(key, 0) or 0) + 1
        GiftedToday[key] = int(GiftedToday.get(key, 0) or 0) + 1
        _action_sync_openness(key)

        if gain > 0:
            result_text = "{} принимает {} заметно теплее, чем можно было ожидать, и явно остается довольна подарком.".format(_action_display_name(key), gift)
        elif gain < 0:
            result_text = "{} принимает {}, но в ее голосе и взгляде ясно слышится прохлада.".format(_action_display_name(key), gift)
        else:
            result_text = "{} принимает {}, вежливо благодарит вас, но особенного впечатления подарок не производит.".format(_action_display_name(key), gift)

        return {
            "ok": True,
            "text": result_text,
            "action_key": "gift",
            "char_name": key,
            "gift_name": gift,
            "gift_item_id": gift_item,
            "friend_delta": gain,
        }

    def family_social_threshold(girl_name="", interaction_type=""):
        key = str(girl_name or "").strip().lower()
        interaction = str(interaction_type or "").strip().lower()
        if key not in ("amanda", "melissa", "sandra"):
            return 0
        if interaction == "flirt":
            return 5
        if interaction in ("gift", "share"):
            return 3
        return 0

    def family_social_threshold_met(girl_name="", interaction_type=""):
        threshold = int(family_social_threshold(girl_name, interaction_type) or 0)
        if threshold <= 0:
            return True
        return int(Friends.get(str(girl_name or "").strip(), 0) or 0) >= threshold

    def player_flirt_with(char_name):
        global fun

        key = str(char_name or "").strip()
        if not key:
            return {"ok": False, "text": "Не с кем флиртовать.", "action_key": "flirt"}

        calendar_advance_minutes(30)
        update_stat_state()

        Talked[key] = int(Talked.get(key, 0) or 0) + 1
        FlirtedToday[key] = int(FlirtedToday.get(key, 0) or 0) + 1
        flirt_gain = resolve_player_social_delta(key, "flirt")
        Friends[key] = max(0, min(20, int(Friends.get(key, 0) or 0) + flirt_gain))
        _action_sync_openness(key)

        fun = _player_clamp(fun + 4, 0, 100)
        if flirt_gain > 0:
            result_text = "Вы немного флиртуете с {} и замечаете ответную реакцию.".format(_action_display_name(key))
        elif flirt_gain < 0:
            result_text = "Вы пытаетесь флиртовать с {}, но это вызывает скорее раздражение.".format(_action_display_name(key))
        else:
            result_text = "Вы немного флиртуете с {}, но ничего особенного не происходит.".format(_action_display_name(key))

        return {
            "ok": True,
            "text": result_text,
            "action_key": "flirt",
            "char_name": key,
            "friend_delta": flirt_gain,
        }

    def current_room_object_menu_label():
        room_obj = CurrentRoom
        if room_obj is None:
            return ""
        room_props = getattr(room_obj, "custom_properties", None)
        if not isinstance(room_props, dict):
            return ""
        return str(room_props.get("object_menu_label", "") or "")


label RefreshCurrentActionMenu(where_id="", object_id="", preserve_text=False):
    $ _refresh_room = str(where_id or getattr(CurrentRoom, "code_name", "") or CurLoc or "").strip()
    $ _refresh_object = str(object_id or current_object_id or "").strip()
    $ _refresh_saved_main = str(MainTxt or "")
    $ _refresh_saved_desc = str(CurLocDesc or "")

    if _refresh_room == "Shed":
        call ShedRoomActions
        return

    if _refresh_room == "Backyard":
        if _refresh_object != "":
            call BackyardObjectMenu(_refresh_object)
            if preserve_text:
                $ MainTxt = _refresh_saved_main
                $ CurLocDesc = _refresh_saved_desc
        else:
            call BackyardBuildActions
        return

    if _refresh_room == "TavernMyRoom":
        if _refresh_object != "":
            call TavernMyRoomObjectMenu(_refresh_object)
            if preserve_text:
                $ MainTxt = _refresh_saved_main
                $ CurLocDesc = _refresh_saved_desc
        else:
            call TavernMyRoomBuildActions
        return

    if _refresh_room == "TavernKitchen":
        if _refresh_object != "":
            call TavernKitchenObjectMenu(_refresh_object)
            if preserve_text:
                $ MainTxt = _refresh_saved_main
                $ CurLocDesc = _refresh_saved_desc
        else:
            call TavernKitchenBuildActions
        return

    if _refresh_room == "TavernAmandaRoom":
        if _refresh_object != "":
            call tavern_amanda_room_object_menu(_refresh_object)
            if preserve_text:
                $ MainTxt = _refresh_saved_main
                $ CurLocDesc = _refresh_saved_desc
        else:
            call TavernAmandaRoomBuildActions
        return

    if _refresh_room == "TavernSandraRoom":
        call TavernSandraRoomBuildActions
        return

    if _refresh_room == "TavernMelissaRoom":
        call TavernMelissaRoomBuildActions
        return

    if _refresh_room == "TavernEmptyRoom":
        call TavernEmptyRoomBuildActions
        return

    if _refresh_room == "TavernAtic":
        if _refresh_object != "":
            call TavernAticObjectMenu(_refresh_object)
            if preserve_text:
                $ MainTxt = _refresh_saved_main
                $ CurLocDesc = _refresh_saved_desc
        else:
            call TavernAticBuildActions
        return

    if _refresh_room == "TavernUpstairs":
        call TavernUpstairsBuildActions
        return

    if _refresh_room == "TavernMain":
        if _refresh_object != "":
            call TavernMainObjectMenu(_refresh_object)
            if preserve_text:
                $ MainTxt = _refresh_saved_main
                $ CurLocDesc = _refresh_saved_desc
        else:
            $ current_action_title = "Действия в трактире"
            $ current_action_content = None
            $ _refresh_room_menu = CurrentRoom.build_menu_sections() if CurrentRoom is not None and hasattr(CurrentRoom, "build_menu_sections") else {"movement": [], "actions": []}
            $ current_action_items = list(_refresh_room_menu.get("movement", [])) + list(_refresh_room_menu.get("actions", []))
        return

    if CurrentRoom is not None:
        $ current_action_title = "Действия"
        $ current_action_content = None
        $ current_action_items = build_room_action_items(CurrentRoom)
    return


label ReturnToMainUI:
    show screen main_ui
    $ request_tractir_autosave("return_ui")
    $ renpy.pause(hard=True)
    return


label Examine(what_id="", where_id="", text_value="", object_id=""):
    $ MainTxt = str(text_value or "")
    $ CurLocDesc = MainTxt
    call RefreshCurrentActionMenu(where_id, object_id or what_id, True)
    return


label Take(what_id="", where_id="", fallback_text="", object_id=""):
    $ item_id = get_object_id(what_id)
    $ _current_room_code = str(getattr(CurrentRoom, "code_name", "") or CurLoc or "")
    if item_id == "":
        $ MainTxt = "Непонятно, что именно вы пытаетесь взять."
        $ CurLocDesc = MainTxt
        return
    if CurrentRoom is None or not _room_has_item_by_id(CurrentRoom, item_id):
        $ MainTxt = "Здесь уже нечего брать."
        $ CurLocDesc = MainTxt
        return
    $ _take_result = take(CurrentRoom, item_id)
    if _take_result.get("ok", False) and _current_room_code == "Shed":
        $ ShedNoticeText = str(_take_result.get("text", ""))
        $ ShedNoticePending = True
    $ MainTxt = str(_take_result.get("text", "") or "Здесь уже нечего брать.")
    if _current_room_code == "Shed":
        $ MainTxt = build_shed_description(True, "")
        call ShedRoomActions
    elif _current_room_code == "TavernMyRoom":
        call TavernMyRoomRestore
    $ CurLocDesc = MainTxt
    call stat
    $ checkpoint_tractir_progress("take_item")
    $ renpy.restart_interaction()
    return


label Drop(what_id="", where_id="", fallback_text="", object_id=""):
    $ item_id = str(what_id or "").strip()
    $ _drop_room_code = str(where_id or getattr(CurrentRoom, "code_name", "") or CurLoc or "").strip()
    if item_id == "" or item_id not in list(game_items or []):
        $ MainTxt = "Непонятно, что именно вы пытаетесь оставить."
        $ CurLocDesc = MainTxt
        return

    $ _drop_result = player_drop_item(CurrentRoom, item_id)
    if _drop_result.get("ok", False):
        if _drop_room_code == "Shed" and item_id == "lumber_001":
            $ _pc_register_chore_success("bring_woods")
        $ MainTxt = str(fallback_text or _drop_result.get("text", "Вы оставляете предмет здесь.") or "Вы оставляете предмет здесь.")
    else:
        $ MainTxt = str(_drop_result.get("text", "У вас этого нет.") or "У вас этого нет.")

    $ CurLocDesc = MainTxt
    call stat
    $ checkpoint_tractir_progress("drop_item")
    call RefreshCurrentActionMenu(where_id, object_id or item_id)
    return


label Drink(what_id="", where_id="", fallback_text="", object_id=""):
    $ item_id = str(what_id or "")
    $ _drink_result = player_drink_item(item_id)
    $ MainTxt = str(_drink_result.get("text", fallback_text) or fallback_text or "")
    $ CurLocDesc = MainTxt
    call stat
    $ checkpoint_tractir_progress("drink_item")
    call RefreshCurrentActionMenu(where_id, object_id, True)
    return


label Eat(item_name="", item_energy=0, fallback_text="", where_id="", object_id=""):
    $ _eat_result = player_eat_meal(item_name, item_energy)
    $ MainTxt = str(_eat_result.get("text", fallback_text) or fallback_text or "")
    $ CurLocDesc = MainTxt
    call stat
    $ checkpoint_tractir_progress("eat_item")
    call RefreshCurrentActionMenu(where_id, object_id)
    return


label Wash(what_id="", where_id="", fallback_text="", object_id=""):
    $ _wash_result = player_wash_with_rainwater()
    $ MainTxt = str(_wash_result.get("text", fallback_text) or fallback_text or "")
    $ CurLocDesc = MainTxt
    call stat
    $ checkpoint_tractir_progress("wash_player")
    call RefreshCurrentActionMenu(where_id, object_id or what_id, True)
    return


label DoChore(chore_key="", where_id="", fallback_text="", object_id=""):
    $ _chore_key = str(chore_key or "").strip()
    $ _chore_result = do_player_chore(_chore_key, where_id, object_id)
    $ MainTxt = str(_chore_result.get("text", fallback_text) or fallback_text or "")
    $ CurLocDesc = MainTxt
    call stat
    $ checkpoint_tractir_progress("do_chore")
    call RefreshCurrentActionMenu(where_id, object_id, True)
    return


label Sleep(return_location="TavernMain", timepassed=1, fallback_text="", where_id="", object_id=""):
    $ _sleep_target = str(return_location or "TavernMain")
    $ _sleep_days = max(1, int(timepassed or 1))
    $ _sleep_where = str(where_id or CurLoc or _sleep_target or "TavernMain")
    $ _sleep_object = str(object_id or current_object_id or "")
    $ calendar_sync_state()
    if not _player_can_sleep_now():
        $ MainTxt = "Еще слишком рано ложиться спать."
        $ CurLocDesc = MainTxt
        call RefreshCurrentActionMenu(_sleep_where, _sleep_object, True)
        return
    if str(fallback_text or "").strip() != "":
        $ MainTxt = str(fallback_text or "").strip()
        $ CurLocDesc = MainTxt
    if melissa_night_wake_event_ready(_sleep_target):
        call MelissaNightWakeEvent
    call NextDay(_sleep_target, _sleep_days)
    if renpy.has_label(_sleep_target):
        jump expression _sleep_target
    return 


label Rest(return_location="", minutes_passed=120, energy_gain=15, fallback_text="", where_id="", object_id=""):
    $ _rest_target = str(return_location or CurLoc or "TavernMyRoom")
    $ _rest_minutes = max(0, int(minutes_passed or 0))
    $ _rest_energy = int(energy_gain or 0)
    $ _rest_text = str(fallback_text or "").strip()
    if _rest_text:
        $ _rest_text = _rest_text + " You feel rested and refreshed!"
    else:
        $ _rest_text = "You feel rested and refreshed!"
    $ MainTxt = _rest_text
    $ CurLocDesc = MainTxt
    $ action_override_text = _rest_text
    if _rest_minutes > 0:
        $ calendar_advance_minutes(_rest_minutes)
    $ update_stat_state()
    $ energy = _player_clamp(energy + _rest_energy, 0, 100)
    call stat
    $ checkpoint_tractir_progress("rest_player")
    call RefreshCurrentActionMenu(where_id or _rest_target, object_id, True)
    return


label MakeFire(what_id="", where_id="", fallback_text="", object_id=""):
    $ _fire_result = do_player_chore("make_fire", where_id, object_id or what_id)
    $ MainTxt = str(_fire_result.get("text", fallback_text) or fallback_text or "")
    $ CurLocDesc = MainTxt
    call stat
    call RefreshCurrentActionMenu(where_id, object_id or what_id, True)
    return


label Clean(what_id="", where_id="", fallback_text="", object_id=""):
    if str(what_id or "") == "ashes":
        $ _clean_result = do_player_chore("clean_ashes", where_id, object_id or what_id)
        $ MainTxt = str(_clean_result.get("text", fallback_text) or fallback_text or "")
    else:
        $ MainTxt = str(fallback_text or "Сейчас это нельзя почистить.")
    $ CurLocDesc = MainTxt
    call stat
    call RefreshCurrentActionMenu(where_id, object_id or what_id, True)
    return


label Chop(what_id="", where_id="", fallback_text="", object_id=""):
    $ item_id = get_object_id(what_id)
    $ _current_room_code = str(getattr(CurrentRoom, "code_name", "") or CurLoc or "")
    if item_id == "":
        $ MainTxt = "Непонятно, что именно вы собираетесь рубить."
        $ CurLocDesc = MainTxt
        return
    if not _player_has_item_by_id("old_axe_001"):
        $ MainTxt = "Без топора колоть дрова не выйдет. Сначала возьмите старый топор."
        $ CurLocDesc = MainTxt
        return
    if CurrentRoom is None:
        $ MainTxt = "Сейчас рубить дрова негде."
        $ CurLocDesc = MainTxt
        return
    if not _room_has_item_by_id(CurrentRoom, item_id) and not _player_has_item_by_id(item_id):
        $ MainTxt = "Колоть сейчас нечего. Сначала нужно принести бревен из леса."
        $ CurLocDesc = MainTxt
        return
    python:
        _used_room_item = _room_has_item_by_id(CurrentRoom, item_id)
        if _used_room_item:
            _room_remove_item_by_id(CurrentRoom, item_id)
        else:
            _player_remove_item_by_id(item_id)
        _room_add_item_units(CurrentRoom, "chopped_wood_001", 10)
        _chop_item = get_game_item(item_id, CurrentRoom)
        _chopped_item = get_game_item("chopped_wood_001", CurrentRoom)
        _chopped_total = _room_item_count_by_id(CurrentRoom, "chopped_wood_001")
        if "_pc_register_chore_success" in globals():
            _pc_register_chore_success("chop_wood")
        calendar_advance_minutes(60)
        update_stat_state()
        fun = _player_clamp(fun + 5, 0, 100)
        energy = _player_clamp(energy - 20, 0, 100)
        exploration = max(0, int(exploration or 0) + 3)
        ShedNoticeText = "Вы нарубили  {}. В сарае теперь есть {}. Всего: {} охапок.".format(str(_chop_item.name).strip(), str(_chopped_item.name).strip(), _chopped_total)
        ShedNoticePending = True
    if _current_room_code == "Shed":
        $ MainTxt = build_shed_description(True, "")
        call ShedRoomActions
    else:
        $ MainTxt = str(ShedNoticeText or "")
    $ CurLocDesc = MainTxt
    call stat
    $ renpy.restart_interaction()
    return


label BoilWater(what_id="", where_id="", fallback_text="", object_id=""):
    $ _boil_result = do_player_chore("boil_water", where_id, object_id or what_id)
    $ MainTxt = str(_boil_result.get("text", fallback_text) or fallback_text or "")
    $ CurLocDesc = MainTxt
    call stat
    call RefreshCurrentActionMenu(where_id, object_id or what_id, True)
    return
