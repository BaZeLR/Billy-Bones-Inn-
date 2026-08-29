# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -46 python:
    _SANDRA_FORAGED_ITEM_IDS = ("berries_001", "mushroom_001", "honey_comb_001")
    _SANDRA_FORAGED_EFFECT_TEXT = "Сандра сразу прикидывает, как пустить это в дело на кухне, и обещает сварить что-нибудь вкусное для всей трактирной челяди."
    _SANDRA_FORAGED_SHARE_TEXT = "Вы отдаете {} {}. Сандра сразу думает, как пустить находку в дело и обещает приготовить для всей трактирной челяди что-нибудь вкусное."
    _ALE_SHARE_BONUS_TARGETS = ("melissa", "amanda")

    SOCIAL_ITEM_EFFECT_RULES = {
        "soap_001": {
            "targets": ("sandra", "melissa", "amanda"),
            "friend_bonus": 3,
            "horny_bonus": 2,
            "beauty_bonus": 20,
            "neshlush_delta": -2,
            "soap_request_threshold": 7,
            "effect_texts": {
                "sandra": "Сандра сразу начинает прикидывать, как такое мыло оценят в трактире, и явно довольна тем, что вы подумали о хозяйстве.",
                "melissa": "Мелисса почти смущенно улыбается, оценив и сам подарок, и то, что вы заметили ее заботу о себе.",
                "amanda": "Аманда принимает мыло с живым интересом и тут же начинает болтать, как приятно будет пахнуть после него.",
            },
            "common_text": "{} сразу заметно хорошеет, становится мягче и послушнее, а чистый запах явно поднимает ей настроение.",
        },
        "luxury_soap_001": {
            "targets": ("sandra", "melissa", "amanda", "becky", "clara"),
            "friend_bonus": 4,
            "horny_bonus": 2,
            "beauty_bonus": 25,
            "effect_texts": {
                "sandra": "Сандра сразу отмечает, что такое мыло годится уже не только для хозяйства, но и для настоящего ухода за собой.",
                "melissa": "Мелисса долго нюхает брусок и признает, что от такого мыла даже настроение становится мягче.",
                "amanda": "Аманда мгновенно начинает болтать о том, как после такого мыла хочется еще и платье, и духи, и новый взгляд на себя.",
                "becky": "Бекки с опытной улыбкой замечает, что хорошее мыло иногда работает лучше любых словесных ухищрений.",
                "clara": "Кларисса оценивает подарок неожиданно серьезно и явно запоминает, что вы умеете подбирать не только грубые полезности.",
            },
            "common_text": "{} сразу заметно оживляется: роскошное мыло действует и на самолюбие, и на настроение.",
        },
        "boar_meat_001": {
            "targets": ("sandra",),
            "friend_bonus": 1,
            "effect_texts": {
                "sandra": "Сандра деловито прикидывает, как лучше разделать мясо, и обещает пустить его на сытный общий стол для домочадцев.",
            },
        },
        "drink_ale_001": {
            "targets": ("amanda", "melissa"),
            "horny_bonus": 1,
            "effect_texts": {
                "amanda": "Аманда быстро веселееет, смеется куда громче обычного и явно рада, что вы решили разделить с ней выпивку.",
                "melissa": "Мелисса отпивает эль осторожно, но вскоре заметно расслабляется и начинает отвечать вам теплее.",
            },
        },
        "energy_tea_001": {
            "targets": ("sandra", "melissa"),
            "effect_texts": {
                "sandra": "Сандра одобрительно кивает: хороший чай явно пришелся кстати среди бесконечных трактирных хлопот.",
                "melissa": "Мелисса благодарит вас за горячий чай и после него охотнее задерживается рядом, не спеша уходить по делам.",
            },
        },
        "libido_tincture_001": {
            "targets": ("clara",),
            "effect_texts": {
                "clara": "Кларисса чуть дольше задерживает на вас взгляд и отвечает заметно более игривым тоном.",
            },
        },
    }

    NPC_ITEM_SHARE_TEXT_RULES = {
        ("drink_ale_001", "default"): "Вы откупориваете бутылку эля и делите ее с {}. Разговор быстро становится проще и веселее.",
        ("energy_tea_001", "default"): "Вы завариваете бодрящий чай для {}. Горячий напиток помогает перевести дух и разговориться.",
        ("libido_tincture_001", "default"): "Вы делитесь пряной настойкой с {}. Напиток приятно разогревает кровь и быстро делает разговор откровеннее.",
        ("boar_meat_001", "sandra"): "Вы приносите {} свежего кабаньего мяса. Сандра тут же прикидывает, что из него выйдет сытный стол для домочадцев, и явно довольна такой добычей.",
        ("luxury_soap_001", "default"): "Вы вручаете {} роскошное мыло. Такой подарок выглядит уже не просто полезным, а почти интимно-заботливым.",
    }

    for _sandra_item_id in _SANDRA_FORAGED_ITEM_IDS:
        SOCIAL_ITEM_EFFECT_RULES[_sandra_item_id] = {
            "targets": ("sandra",),
            "friend_bonus": 1,
            "fun_bonus": 1,
            "effect_texts": {
                "sandra": _SANDRA_FORAGED_EFFECT_TEXT,
            },
        }
        NPC_ITEM_SHARE_TEXT_RULES[(_sandra_item_id, "sandra")] = _SANDRA_FORAGED_SHARE_TEXT

    def record_breakfast_share_perk(char_name="", item_id=""):
        key = str(char_name or "").strip().lower()
        item_key = str(item_id or "").strip()
        if key not in ("sandra", "melissa", "amanda"):
            return

        perks = player.tavern_management.breakfast_share_perks

        score = 1
        if item_key in ("honey_comb_001", "berries_001", "milk_pitcher_001"):
            score = 2
        if item_key in ("drink_ale_001", "energy_tea_001", "libido_tincture_001"):
            score = 2
        if item_key in ("luxury_soap_001",):
            score = 3

        existing = perks.get(key, {})
        existing_score = int(existing.get("score", 0) or 0) if isinstance(existing, dict) else 0
        perks[key] = {
            "day": int(current_game_day()),
            "item": item_key,
            "score": max(existing_score, score),
        }

    def clamp_stat(value, low, high):
        return max(int(low or 0), min(int(high or 0), int(value or 0)))

    def add_to_stat_dict(table, key, delta, low, high):
        if not isinstance(table, dict):
            return 0
        target_key = str(key or "").strip()
        if target_key == "":
            return 0
        next_value = clamp_stat(int(table.get(target_key, 0) or 0) + int(delta or 0), low, high)
        table[target_key] = next_value
        return next_value

    def social_score_delta_for(char_name="", before_value=0):
        key = str(char_name or "").strip()
        info = people.get_info(key)
        current_value = int(getattr(info, "rel", 0) or 0) if info is not None else 0
        return current_value - int(before_value or 0)

    def social_score_message(score_delta=0):
        value = int(score_delta or 0)
        if value > 0:
            return "Очки отношений: +{}.".format(value)
        if value < 0:
            return "Очки отношений: {}.".format(value)
        return "Очки отношений: 0."

    def notify_social_score(score_delta=0):
        try:
            renpy.notify(social_score_message(score_delta))
        except Exception:
            pass
        return int(score_delta or 0)

    def append_social_score_message(text="", score_delta=0, notify=True):
        if bool(notify):
            notify_social_score(score_delta)
        base_text = str(text or "").strip()
        score_text = social_score_message(score_delta)
        if base_text:
            return base_text + "\n\n" + score_text
        return score_text

    def _player_clamp(value, low, high):
        return clamp_stat(value, low, high)

    def action_restriction_text(mode=None, hunger_floor=None, late_hour_range=(4, 5), fun_floor=None):
        try:
            current_hour = int(calendar_v2.hour or 0)
        except Exception:
            current_hour = 0

        if late_hour_range is not None:
            try:
                late_start = int(late_hour_range[0])
                late_end = int(late_hour_range[1])
            except Exception:
                late_start = 4
                late_end = 5
            if late_start <= current_hour <= late_end:
                return "Я слишком вымотан. Уже слишком поздно, пора немедленно ложиться спать."

        requested_mode = str(mode or "").strip().lower()
        effective_fun_floor = fun_floor
        if effective_fun_floor is None:
            if requested_mode == "fun40":
                effective_fun_floor = 40
            elif requested_mode == "fun60":
                effective_fun_floor = 60
        if effective_fun_floor is not None:
            try:
                current_fun = int(player.condition.fun or 0)
            except Exception:
                current_fun = 0
            if current_fun < int(effective_fun_floor):
                return "Я сейчас не в том настроении, чтобы этим заниматься."

        return ""

    def restrictions(mode=None, hunger_floor=None, late_hour_range=(4, 5), fun_floor=None):
        return str(action_restriction_text(mode, hunger_floor, late_hour_range, fun_floor) or "").strip() != ""

    ACTION_RESTRICTION_RULES = {
        "chore": {"energy_floor": 20, "late_hour_range": (4, 5), "text": "Я слишком вымотан, чтобы заниматься этим прямо сейчас."},
        "heavy_chore": {"energy_floor": 30, "late_hour_range": (4, 5), "text": "Я слишком вымотан для такой тяжелой работы прямо сейчас."},
        "wash": {"energy_floor": 5, "late_hour_range": (4, 5), "text": "Я слишком вымотан, чтобы сейчас возиться с умыванием."},
        "rest": {"energy_floor": 5, "late_hour_range": (4, 5), "text": "Сейчас уже не отдыхать надо, а нормально ложиться спать."},
        "fun40": {"energy_floor": 10, "late_hour_range": (4, 5), "fun_floor": 40},
        "fun60": {"energy_floor": 10, "late_hour_range": (4, 5), "fun_floor": 60},
    }

    # Chore action identifiers + weekly targets (counters live in player.chores.weekly, defaulted in script.rpy)
    # These are the "chores" that have energy/time restrictions above and are tracked for Sandra's weekly review.
    PLAYER_CHORE_KEYS = (
        "bring_woods",
        "chop_wood",
        "make_fire",
        "clean_ashes",
        "boil_water",
        "clean_upstairs_rooms",
    )
    PLAYER_CHORE_TARGETS = {
        "bring_woods": 3,
        "chop_wood": 3,
        "make_fire": 3,
        "clean_ashes": 3,
        "boil_water": 7,
        "clean_upstairs_rooms": 3,
    }

    STANDARD_ACTION_METHODS = {
        "take": {"hook": "call", "target": "Take", "label": "Взять"},
        "drop": {"hook": "call", "target": "Drop", "label": "Оставить"},
        "drink": {"hook": "call", "target": "Drink", "label": "Выпить"},
        "eat": {"hook": "call", "target": "EatItem", "label": "Съесть"},
        "meal": {"hook": "call", "target": "Eat", "label": "Поесть"},
        "wash": {"hook": "call", "target": "Wash", "label": "Умыться"},
        "chore": {"hook": "call", "target": "DoChore", "label": "Поработать"},
        "sleep": {"hook": "call", "target": "Sleep", "label": "Спать"},
        "rest": {"hook": "call", "target": "Rest", "label": "Отдохнуть"},
        "make_fire": {"hook": "call", "target": "MakeFire", "label": "Разжечь огонь"},
        "clean": {"hook": "call", "target": "Clean", "label": "Почистить"},
        "chop": {"hook": "call", "target": "Chop", "label": "Колоть"},
    }

    def standard_action_profile(action_key=""):
        key = str(action_key or "").strip().lower()
        return dict(STANDARD_ACTION_METHODS.get(key, {}) or {})

    def make_standard_object_action(action_key="", label="", args=None, condition=None, custom_properties=None, action_id="", target="", hook=""):
        key = str(action_key or "").strip().lower()
        profile = standard_action_profile(key)
        if not profile and not target:
            return None

        action_label = str(label or profile.get("label", key) or key)
        action_target = str(target or profile.get("target", "") or "")
        action_hook = str(hook or profile.get("hook", "call") or "call")
        action_args = tuple(args or ())
        if not action_target:
            return None

        props = dict(custom_properties or {})
        props.setdefault("standard_action", key)

        resolved_action_id = str(action_id or "").strip()
        if not resolved_action_id:
            id_parts = [key, action_target]
            for raw_arg in action_args[:2]:
                raw_text = str(raw_arg or "").strip()
                if raw_text:
                    id_parts.append(raw_text)
            resolved_action_id = "_".join(id_parts)

        return ObjectAction(
            action_id=resolved_action_id,
            label=action_label,
            hook=action_hook,
            target=action_target,
            args=action_args,
            condition=condition,
            custom_properties=props,
        )

    def make_take_action(object_id="", where_id="", fallback_text="", label="", condition=None):
        return make_standard_object_action(
            "take",
            label or "Взять",
            (object_id, where_id, fallback_text),
            condition,
            {"object_id": str(object_id or ""), "where_id": str(where_id or "")},
        )

    def make_consume_item_action(object_id="", action_key="eat", where_id="", label="", fallback_text="", condition=None):
        use_key = str(action_key or "eat").strip().lower()
        default_label = "Выпить" if use_key == "drink" else "Съесть"
        target_label = "Drink" if use_key == "drink" else "EatItem"
        return make_standard_object_action(
            use_key,
            label or default_label,
            (object_id, where_id, fallback_text, object_id),
            condition,
            {"object_id": str(object_id or ""), "where_id": str(where_id or ""), "consume_action": use_key},
            target=target_label,
        )

    def make_meal_action(item_name="", item_energy=0, where_id="", object_id="", label="", fallback_text="", condition=None):
        return make_standard_object_action(
            "meal",
            label or "Поесть",
            (item_name, item_energy, fallback_text, where_id, object_id),
            condition,
            {"object_id": str(object_id or ""), "where_id": str(where_id or ""), "item_name": str(item_name or "")},
        )

    def make_chore_action(chore_key="", where_id="", label="", fallback_text="", object_id="", condition=None):
        return make_standard_object_action(
            "chore",
            label or "Поработать",
            (chore_key, where_id, fallback_text, object_id),
            condition,
            {"chore_key": str(chore_key or ""), "where_id": str(where_id or ""), "object_id": str(object_id or "")},
        )

    def make_sleep_action(return_location="TavernMain", days=1, label="", fallback_text="", where_id="", object_id="", condition=None):
        return make_standard_object_action(
            "sleep",
            label or "Спать",
            (return_location, days, fallback_text, where_id, object_id),
            condition,
            {"return_location": str(return_location or ""), "where_id": str(where_id or ""), "object_id": str(object_id or "")},
        )

    def make_rest_action(return_location="", minutes_passed=120, energy_gain=15, label="", fallback_text="", where_id="", object_id="", condition=None):
        return make_standard_object_action(
            "rest",
            label or "Отдохнуть",
            (return_location, minutes_passed, energy_gain, fallback_text, where_id, object_id),
            condition,
            {"return_location": str(return_location or ""), "where_id": str(where_id or ""), "object_id": str(object_id or "")},
        )

    def make_simple_target_action(action_key="", object_id="", where_id="", label="", fallback_text="", condition=None):
        key = str(action_key or "").strip().lower()
        return make_standard_object_action(
            key,
            label or str(standard_action_profile(key).get("label", key) or key),
            (object_id, where_id, fallback_text, object_id),
            condition,
            {"object_id": str(object_id or ""), "where_id": str(where_id or "")},
        )

    def action_restriction_message(action_type=""):
        action_key = str(action_type or "").strip().lower()
        profile = dict(ACTION_RESTRICTION_RULES.get(action_key, {}) or {})
        restriction_text = str(action_restriction_text(action_key, None, profile.get("late_hour_range", (4, 5)), profile.get("fun_floor", None)) or "").strip()
        if restriction_text != "":
            return restriction_text

        energy_floor = profile.get("energy_floor", None)
        if energy_floor is not None:
            try:
                current_energy = int(player.condition.energy or 0)
            except Exception:
                current_energy = 0
            if current_energy < int(energy_floor):
                return str(profile.get("text", "") or "Я слишком вымотан, чтобы заниматься этим прямо сейчас.").strip()
        return ""

    def action_is_restricted(action_type=""):
        return str(action_restriction_message(action_type) or "").strip() != ""

    def action_restriction_result(action_type="", action_key=""):
        message = str(action_restriction_message(action_type) or "").strip()
        if message == "":
            return {"ok": True, "text": "", "action_key": str(action_key or action_type or "").strip()}
        return {"ok": False, "text": message, "action_key": str(action_key or action_type or "").strip()}

    def _player_inventory_snapshot():
        return dict(player.inventory.items or {})

    def _player_restore_inventory_deficit(snapshot, exempt_ids=None):
        expected = dict(snapshot or {})
        if not expected:
            return dict(player.inventory.items or {})

        exempt = set()
        for raw_item_id in tuple(exempt_ids or ()):
            item_key = get_object_id(raw_item_id)
            if item_key:
                exempt.add(item_key)

        current = dict(player.inventory.items or {})

        for item_key, raw_expected_count in list(expected.items()):
            if item_key in exempt:
                continue
            try:
                expected_count = max(0, int(raw_expected_count or 0))
            except (TypeError, ValueError):
                expected_count = 0
            if expected_count <= 0:
                continue
            current_count = max(0, int(current.get(item_key, 0) or 0))
            if current_count < expected_count:
                current[item_key] = expected_count
        player.inventory.items = player_normalize_inventory(current)
        return dict(current)

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

        return removed

    def _room_add_item_by_id(room_obj, item_id):
        if room_obj is None or not hasattr(room_obj, "game_items"):
            return False

        item_id = get_object_id(item_id)
        if not item_id:
            return False

        room_obj.game_items.append(item_id)
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
        current_hour = int(calendar_v2.hour or 0)
        return current_hour >= 20 or current_hour < 6

    def player_sleep_wake_time():
        current_hour = int(calendar_v2.hour or 0)
        current_minute = int(calendar_v2.minute or 0)
        if int(player.sleep_wake_hour_override or -1) >= 0:
            return (int(player.sleep_wake_hour_override or 0) % 24, int(player.sleep_wake_minute_override or 0) % 60)
        if current_hour >= 23:
            return (6, 0)
        if current_hour < 6:
            return (max(7, min(9, current_hour + 5)), current_minute)
        return (6, 0)

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
        except (AttributeError, TypeError, ValueError):
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

    def _action_display_name(char_name):
        key = str(char_name or "").strip()
        if not key:
            return ""
        return str(people_display_name(key) or key)

    def _player_item_consume_profile(item_id, expected_action=""):
        item_key = str(get_object_id(item_id) or "").strip()
        item_obj = get_game_item(item_key)
        if item_obj is None:
            return None

        custom_props = dict(getattr(item_obj, "custom_properties", {}) or {})
        action_key = str(expected_action or custom_props.get("consume_action", "") or "").strip()
        if action_key == "":
            return None

        outputs = []
        for raw_output in list(custom_props.get("consume_outputs", ()) or ()):
            if isinstance(raw_output, dict):
                output_id = str(get_object_id(raw_output.get("item_id", "")) or "").strip()
                output_qty = int(raw_output.get("quantity", 1) or 1)
            elif isinstance(raw_output, (list, tuple)) and len(raw_output) >= 1:
                output_id = str(get_object_id(raw_output[0]) or "").strip()
                output_qty = int((raw_output[1] if len(raw_output) > 1 else 1) or 1)
            else:
                output_id = str(get_object_id(raw_output) or "").strip()
                output_qty = 1
            if output_id and output_qty > 0:
                outputs.append((output_id, output_qty))

        return {
            "item_id": item_key,
            "item_obj": item_obj,
            "action_key": action_key,
            "minutes": int(custom_props.get("consume_minutes", 0) or 0),
            "energy_gain": int(custom_props.get("consume_energy", 0) or 0),
            "fun_gain": int(custom_props.get("consume_fun", 0) or 0),
            "text": str(custom_props.get("consume_text", "") or "").strip(),
            "outputs": outputs,
        }

    def _player_apply_item_consume_profile(item_id, expected_action="", consume_from_inventory=False):

        item_key = str(get_object_id(item_id) or "").strip()
        action_key = str(expected_action or "").strip()
        if item_key == "" or action_key == "":
            return {
                "ok": False,
                "text": "Сейчас это нельзя использовать.",
                "action_key": action_key,
                "item_id": item_key,
            }

        profile = _player_item_consume_profile(item_key, action_key)
        if profile is None or str(profile.get("action_key", "") or "") != action_key:
            failure_text = "Сейчас это нельзя выпить." if action_key == "drink" else "Сейчас это нельзя съесть."
            return {
                "ok": False,
                "text": failure_text,
                "action_key": action_key,
                "item_id": item_key,
            }

        if consume_from_inventory:
            missing_text = "Этого напитка у вас при себе больше нет." if action_key == "drink" else "Этой еды у вас при себе больше нет."
            if player.item_count(item_key) <= 0:
                return {
                    "ok": False,
                    "text": missing_text,
                    "action_key": action_key,
                    "item_id": item_key,
                }
            if not player.remove_item(item_key, 1):
                return {
                    "ok": False,
                    "text": missing_text,
                    "action_key": action_key,
                    "item_id": item_key,
                }

        minutes_cost = max(0, int(profile.get("minutes", 0) or 0))
        if minutes_cost > 0:
            calendar_v2.advance_minutes(minutes_cost)

        player.change_stat("energy", int(profile.get("energy_gain", 0) or 0))
        player.change_stat("fun", int(profile.get("fun_gain", 0) or 0))

        for output_id, output_qty in list(profile.get("outputs", []) or []):
            player.add_item(output_id, output_qty)

        update_stat_state()

        item_name = str(getattr(profile.get("item_obj", None), "name", "") or item_key).strip() or item_key
        result_text = str(profile.get("text", "") or "").strip()
        if result_text == "":
            if action_key == "drink":
                result_text = "Вы выпиваете {}.".format(item_name)
            else:
                result_text = "Вы съедаете {}.".format(item_name)

        return {
            "ok": True,
            "text": result_text,
            "action_key": action_key,
            "item_id": item_key,
            "item_name": item_name,
        }

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

        player.add_item(item_id)
        game_item = get_game_item(item_id, room_obj)
        take_text = "Вы берете {}.".format(str(game_item.name).strip())

        return {
            "ok": True,
            "text": take_text,
            "action_key": "take",
            "item_id": item_id,
        }

    def player_pick_up_item(room_obj, item_id):
        return take(room_obj, item_id)

    def player_drop_item(room_obj, item_id):
        item_key = str(item_id or "").strip()
        if not item_key:
            return {
                "ok": False,
                "text": "Нечего бросать.",
                "action_key": "drop",
                "item_id": item_key,
            }

        removed = player.remove_item(item_key)
        if not removed:
            return {
                "ok": False,
                "text": "У вас этого нет.",
                "action_key": "drop",
                "item_id": item_key,
            }

        added = _room_add_item_by_id(room_obj, item_key)
        if not added:
            player.add_item(item_key)
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
        item_key = str(item_id or "").strip()
        if not item_key:
            return {
                "ok": False,
                "text": "Пить нечего.",
                "action_key": "drink",
                "item_id": item_key,
            }
        return dict(player_use_item(item_key, "drink", False) or {})

    def player_eat_item(item_id):
        item_key = str(item_id or "").strip()
        if not item_key:
            return {
                "ok": False,
                "text": "Есть сейчас нечего.",
                "action_key": "eat",
                "item_id": item_key,
            }
        return dict(player_use_item(item_key, "eat", False) or {})

    def player_use_item(item_id, action_key="", consume_from_inventory=False):
        item_key = str(item_id or "").strip()
        use_key = str(action_key or "").strip()
        if not item_key or not use_key:
            return {
                "ok": False,
                "text": "Сейчас это нельзя использовать.",
                "action_key": use_key,
                "item_id": item_key,
            }
        return dict(_player_apply_item_consume_profile(item_key, use_key, consume_from_inventory) or {})

    def apply_social_interaction_base(char_name="", interaction_type="", friend_delta=0, fun_delta=0, minutes_cost=0, talked_delta=0, flirted_today_delta=0, gifted_today_delta=0, talked_today_delta=0):

        key = str(char_name or "").strip()
        if key == "":
            return

        if int(minutes_cost or 0) > 0:
            calendar_v2.advance_minutes(int(minutes_cost or 0))
            update_stat_state()

        info = people.get_info(key)
        talk_increment = max(int(talked_delta or 0), int(talked_today_delta or 0))
        if info is not None and talk_increment != 0:
            info.mark_talked(talk_increment)
        if info is not None and int(flirted_today_delta or 0) != 0:
            info.flirted_today = max(0, int(info.flirted_today or 0) + int(flirted_today_delta or 0))
        if info is not None and int(gifted_today_delta or 0) != 0:
            info.gifted_today = max(0, int(info.gifted_today or 0) + int(gifted_today_delta or 0))
        if info is not None and int(friend_delta or 0) != 0:
            info.change_social(friend_delta=int(friend_delta or 0))
        if int(fun_delta or 0) != 0:
            player.change_stat("fun", int(fun_delta or 0))

    def _social_item_rule(item_id="", char_name=""):
        item_key = str(item_id or "").strip()
        char_key = str(char_name or "").strip()
        rule = dict(SOCIAL_ITEM_EFFECT_RULES.get(item_key, {}) or {})
        targets = tuple(rule.get("targets", ()) or ())
        if targets and char_key not in targets:
            return {}
        return rule

    def _social_item_effect_lines(char_name="", item_id=""):
        key = str(char_name or "").strip()
        item_key = str(item_id or "").strip()
        rule = _social_item_rule(item_key, key)
        if not rule:
            return []
        lines = []
        common_text = str(rule.get("common_text", "") or "").strip()
        if common_text:
            lines.append(common_text.format(_action_display_name(key)))
        effect_text = str(dict(rule.get("effect_texts", {}) or {}).get(key, "") or "").strip()
        if effect_text:
            lines.append(effect_text)
        info = people.get_info(key)
        if item_key == "soap_001" and info is not None and int(info.rel or 0) >= int(rule.get("soap_request_threshold", 999) or 999):
            lines.append("Похоже, ей так нравится это мыло, что потом она наверняка попросит у вас еще.")
        return lines

    def player_apply_item_social_effects(char_name="", item_id="", from_gift=False):

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

        rule = _social_item_rule(item_key, key)
        info = people.get_info(key)

        if from_gift:
            if info is not None and friend_bonus > 0:
                info.change_social(friend_delta=friend_bonus)
            if fun_bonus > 0:
                player.change_stat("fun", fun_bonus)
            if info is not None and openness_bonus > 0:
                info.change_social(open_delta=openness_bonus)
            if trust_bonus > 0 and key == "clara":
                Clara.trust = clamp_stat(int(Clara.trust or 0) + trust_bonus, 0, 20)
            if info is not None and horny_bonus > 0:
                info.change_social(corruption_delta=horny_bonus)

            if rule:
                if info is not None and int(rule.get("friend_bonus", 0) or 0) != 0:
                    info.change_social(friend_delta=int(rule.get("friend_bonus", 0) or 0))
                if int(rule.get("fun_bonus", 0) or 0) != 0 and fun_bonus <= 0:
                    player.change_stat("fun", int(rule.get("fun_bonus", 0) or 0))
                if info is not None and int(rule.get("beauty_bonus", 0) or 0) != 0:
                    info.set_sex_stat("beauty", max(0, min(100, int(info.sex_stat("beauty", 0) or 0) + int(rule.get("beauty_bonus", 0) or 0))))
                if info is not None and int(rule.get("horny_bonus", 0) or 0) != 0:
                    info.change_social(corruption_delta=int(rule.get("horny_bonus", 0) or 0))
                if info is not None and int(rule.get("neshlush_delta", 0) or 0) != 0:
                    info.rebel_baseline = max(0, int(info.rebel_baseline or 0) + int(rule.get("neshlush_delta", 0) or 0))
                if item_key == "soap_001" and info is not None and int(info.rel or 0) >= int(rule.get("soap_request_threshold", 999) or 999):
                    crafting.soap_requests[key] = 1

        effect_lines = []
        if fun_bonus > 0:
            effect_lines.append("{} заметно расслабляется и охотнее поддерживает разговор.".format(_action_display_name(key)))
        if openness_bonus > 0:
            effect_lines.append("{} делится чем-то более личным и говорит куда откровеннее обычного.".format(_action_display_name(key)))
        if trust_bonus > 0 and key == "clara":
            effect_lines.append("Похоже, Кларисса начинает доверять вам заметно больше.")
        if horny_bonus > 0:
            effect_lines.append("От подарка в ее глазах появляется теплый, немного шальной блеск.")
        effect_lines.extend(_social_item_effect_lines(key, item_key))

        return {
            "text": " ".join(effect_lines).strip(),
            "friend_bonus": friend_bonus,
            "openness_bonus": openness_bonus,
            "trust_bonus": trust_bonus,
            "horny_bonus": horny_bonus,
        }

    def player_share_item_with(char_name="", item_id=""):

        key = str(char_name or "").strip()
        item_key = str(item_id or "").strip()
        item_obj = get_game_item(item_key)
        if key == "" or item_obj is None:
            return {"ok": False, "text": "Сейчас этим нельзя ни с кем поделиться.", "action_key": "share"}
        allowed, reason = relationship_social_action_allowed(key, "share", item_key)
        if not allowed:
            relationship_after_social_result(key, "share", -1, False)
            return {"ok": False, "text": str(reason or relationship_block_text(key, "share")), "action_key": "share", "char_name": key, "item_id": item_key}

        custom_props = dict(getattr(item_obj, "custom_properties", {}) or {})
        item_kind = str(custom_props.get("item_kind", "") or "").strip()
        loot_kind = str(custom_props.get("loot_kind", "") or "").strip()
        share_allowed = False
        try:
            share_allowed = bool(player_card_is_shareable_item(item_key))
        except (AttributeError, NameError, TypeError, ValueError):
            share_allowed = (
                item_kind in ("forest_resource", "animal_loot", "crafted_good")
                or str(custom_props.get("crafted_kind", "") or "").strip() != ""
                or (item_kind == "animal_loot" and loot_kind != "")
            )
        if not share_allowed:
            return {"ok": False, "text": "Сейчас этим делиться не очень уместно.", "action_key": "share"}

        removed = player.remove_item(item_key, 1)
        if not removed:
            return {"ok": False, "text": "Этой вещи у вас больше нет.", "action_key": "share"}

        if item_key == "drink_ale_001":
            player.add_item("empty_bottle_001", 1)
            player.add_item("cork_001", 1)

        base_friend = max(1, int(custom_props.get("gift_value", 1) or 1))
        base_friend = relationship_adjust_social_score(key, "share", resolve_player_social_delta(key, "share", base_friend, item_key))
        apply_social_interaction_base(key, "share", base_friend, max(1, int(custom_props.get("social_fun_bonus", 0) or 0)), 0, 1, 0, 1, 1)
        effect_result = player_apply_item_social_effects(key, item_key, True)
        record_breakfast_share_perk(key, item_key)

        share_text = "{} принимает угощение и вы проводите вместе несколько спокойных минут.".format(_action_display_name(key))
        share_rule = str(NPC_ITEM_SHARE_TEXT_RULES.get((item_key, key), "") or NPC_ITEM_SHARE_TEXT_RULES.get((item_key, "default"), "") or "").strip()
        if share_rule != "":
            if "{} {}" in share_rule or " {}." in share_rule:
                share_text = share_rule.format(_action_display_name(key), getattr(item_obj, "name", item_key))
            else:
                share_text = share_rule.format(_action_display_name(key))

        if item_key == "drink_ale_001" and key in _ALE_SHARE_BONUS_TARGETS:
            target_info = people.get_info(key)
            if target_info is not None:
                target_info.change_social(corruption_delta=1)

        result_text = share_text
        if str(effect_result.get("text", "") or "").strip():
            result_text += " " + str(effect_result.get("text", "") or "").strip()
        relationship_after_social_result(key, "share", base_friend, True)
        try:
            player_social_condition_notify(key)
        except Exception:
            pass

        return {
            "ok": True,
            "text": result_text,
            "action_key": "share",
            "char_name": key,
            "item_id": item_key,
        }

    def player_eat_meal(item_name, item_energy, minutes_to_pass=30):

        item_label = str(item_name or "еду").strip() or "еду"
        energy_gain = max(0, int(item_energy or 0))
        meal_minutes = max(0, int(minutes_to_pass or 0))

        calendar_v2.advance_minutes(meal_minutes)
        update_stat_state()
        player.change_stat("energy", energy_gain)
        player.change_stat("fun", 5)

        return {
            "ok": True,
            "text": "Вы съедаете {} и чувствуете, как силы понемногу возвращаются.".format(item_label),
            "action_key": "eat",
            "item_name": item_label,
            "item_energy": energy_gain,
        }

    def player_wash_with_rainwater():

        calendar_v2.advance_minutes(30)
        player.appearance.wash()
        update_stat_state()
        player.change_stat("energy", -5)

        return {
            "ok": True,
            "text": "Вы умываетесь и наскоро обмываетесь холодной дождевой водой. Это освежает и помогает привести себя в порядок.",
            "action_key": "wash",
        }

    def player_talk_to(char_name):
        key = str(char_name or "").strip()
        if not key:
            return {"ok": False, "text": "Не с кем разговаривать.", "action_key": "talk"}

        info = people.get_info(key)
        friends_before = int(getattr(info, "rel", 0) or 0) if info is not None else 0
        friend_gain = relationship_adjust_social_score(key, "talk", resolve_player_social_delta(key, "talk"))
        apply_social_interaction_base(key, "talk", friend_gain, 2, 30, 1, 0, 0, 1)
        relationship_after_social_result(key, "talk", friend_gain, True)
        actual_gain = social_score_delta_for(key, friends_before)
        if friend_gain > 0:
            result_text = "Вы некоторое время беседуете с {}. Разговор проходит заметно теплее обычного.".format(_action_display_name(key))
        elif friend_gain < 0:
            result_text = "Вы пытаетесь побеседовать с {}, но разговор выходит не слишком удачным.".format(_action_display_name(key))
        else:
            result_text = "Вы некоторое время беседуете с {}.".format(_action_display_name(key))
        result_text = append_social_score_message(result_text, actual_gain)
        try:
            player_social_condition_notify(key)
        except Exception:
            pass

        return {
            "ok": True,
            "text": result_text,
            "action_key": "talk",
            "char_name": key,
            "friend_delta": actual_gain,
            "raw_friend_delta": friend_gain,
        }

    def player_gift_to(char_name, gift_name="подарок", friend_gain=2, gift_item_id="", include_score_message=True):
        key = str(char_name or "").strip()
        gift = str(gift_name or "подарок").strip()
        gift_item = str(gift_item_id or "").strip()
        gain = int(friend_gain or 2)
        if not key:
            return {"ok": False, "text": "Некому дарить подарок.", "action_key": "gift"}

        info = people.get_info(key)
        friends_before = int(getattr(info, "rel", 0) or 0) if info is not None else 0
        allowed, reason = relationship_social_action_allowed(key, "gift", gift_item)
        if not allowed:
            apply_social_interaction_base(key, "gift", -1, 0, 0, 1, 0, 1, 0)
            relationship_after_social_result(key, "gift", -2, False)
            result_text = str(reason or relationship_block_text(key, "gift"))
            if include_score_message:
                result_text = append_social_score_message(result_text, social_score_delta_for(key, friends_before))
                try:
                    player_social_condition_notify(key)
                except Exception:
                    pass
            return {
                "ok": False,
                "text": result_text,
                "action_key": "gift",
                "char_name": key,
                "gift_name": gift,
                "gift_item_id": gift_item,
                "friend_delta": social_score_delta_for(key, friends_before),
                "raw_friend_delta": -2,
            }
        gain = resolve_player_social_delta(key, "gift", gain, gift_item)
        try:
            preferred_items = list(preferred_gift_item_ids(key) or [])
        except (AttributeError, NameError, TypeError, ValueError):
            preferred_items = []
        if gift_item != "" and gift_item in preferred_items:
            gain = max(1, int(gain or 0))
        elif gift_item == "libido_tincture_001" and key == "clara":
            gain = max(1, int(gain or 0))
        try:
            gift_accepts, gift_score = social_gift_acceptance(key, gift_item, gain)
        except Exception:
            gift_accepts, gift_score = True, gain
        if not gift_accepts:
            apply_social_interaction_base(key, "gift", int(gift_score or 0), 0, 0, 1, 0, 1, 0)
            relationship_after_social_result(key, "gift", int(gift_score or 0), False)
            actual_gain = social_score_delta_for(key, friends_before)
            result_text = social_gift_text(key, gift, gift_item, gift_score)
            if include_score_message:
                result_text = append_social_score_message(result_text, actual_gain)
                try:
                    player_social_condition_notify(key)
                except Exception:
                    pass
            return {
                "ok": False,
                "text": result_text,
                "action_key": "gift",
                "char_name": key,
                "gift_name": gift,
                "gift_item_id": gift_item,
                "friend_delta": actual_gain,
                "raw_friend_delta": int(gift_score or 0),
            }
        gain = int(gift_score or gain)
        apply_social_interaction_base(key, "gift", gain, 0, 0, 1, 0, 1, 0)
        relationship_after_social_result(key, "gift", gain, True)
        actual_gain = social_score_delta_for(key, friends_before)

        try:
            result_text = social_gift_text(key, gift, gift_item, gain)
        except Exception:
            if gain > 0:
                result_text = "{} принимает {} заметно теплее, чем можно было ожидать, и явно остается довольна подарком.".format(_action_display_name(key), gift)
            elif gain < 0:
                result_text = "{} принимает {}, но в ее голосе и взгляде ясно слышится прохлада.".format(_action_display_name(key), gift)
            else:
                result_text = "{} принимает {}, вежливо благодарит вас, но особенного впечатления подарок не производит.".format(_action_display_name(key), gift)
        if include_score_message:
            result_text = append_social_score_message(result_text, actual_gain)
            try:
                player_social_condition_notify(key)
            except Exception:
                pass

        return {
            "ok": True,
            "text": result_text,
            "action_key": "gift",
            "char_name": key,
            "gift_name": gift,
            "gift_item_id": gift_item,
            "friend_delta": actual_gain,
            "raw_friend_delta": gain,
        }

    def family_social_threshold(girl_name="", interaction_type=""):
        key = str(girl_name or "").strip().lower()
        interaction = str(interaction_type or "").strip().lower()
        if key not in ("amanda", "melissa", "sandra"):
            return 0
        return relationship_requirement_value(key, interaction, "score")

    def family_social_threshold_met(girl_name="", interaction_type=""):
        key = str(girl_name or "").strip()
        interaction = str(interaction_type or "").strip().lower()
        if interaction == "gift":
            return relationship_any_gift_allowed(key)
        allowed, reason = relationship_social_action_allowed(key, interaction_type)
        return bool(allowed)

    def player_flirt_with(char_name):
        key = str(char_name or "").strip()
        if not key:
            return {"ok": False, "text": "Не с кем флиртовать.", "action_key": "flirt"}

        allowed, reason = relationship_social_action_allowed(key, "flirt")
        if not allowed:
            relationship_after_social_result(key, "flirt", -1, False)
            return {"ok": False, "text": str(reason or relationship_block_text(key, "flirt")), "action_key": "flirt", "char_name": key, "friend_delta": 0, "raw_friend_delta": -1}

        info = people.get_info(key)
        friends_before = int(getattr(info, "rel", 0) or 0) if info is not None else 0
        flirt_gain = relationship_adjust_social_score(key, "flirt", resolve_player_social_delta(key, "flirt"))
        apply_social_interaction_base(key, "flirt", flirt_gain, 4, 30, 1, 1, 0, 0)
        relationship_after_social_result(key, "flirt", flirt_gain, True)
        actual_gain = social_score_delta_for(key, friends_before)
        if flirt_gain > 0:
            result_text = "Вы немного флиртуете с {} и замечаете ответную реакцию.".format(_action_display_name(key))
        elif flirt_gain < 0:
            result_text = "Вы пытаетесь флиртовать с {}, но это вызывает скорее раздражение.".format(_action_display_name(key))
        else:
            result_text = "Вы немного флиртуете с {}, но ничего особенного не происходит.".format(_action_display_name(key))
        result_text = append_social_score_message(result_text, actual_gain)
        try:
            player_social_condition_notify(key)
        except Exception:
            pass

        return {
            "ok": True,
            "text": result_text,
            "action_key": "flirt",
            "char_name": key,
            "friend_delta": actual_gain,
            "raw_friend_delta": flirt_gain,
        }

label Take(what_id="", where_id="", fallback_text="", object_id=""):
    $ renpy.dynamic("item_id", "_current_room_code", "_take_result")
    $ item_id = get_object_id(what_id)
    $ _current_room_code = str(getattr(rooms.current, "code_name", "") or rooms.current_code or "")
    if item_id == "":
        $ scene_runtime.text = "Непонятно, что именно вы пытаетесь взять."
        $ scene_runtime.location_text = scene_runtime.text
        return
    if rooms.current is None or not _room_has_item_by_id(rooms.current, item_id):
        $ scene_runtime.text = "Здесь уже нечего брать."
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ _take_result = take(rooms.current, item_id)
    if _take_result.get("ok", False) and _current_room_code == "Shed":
        $ rooms.get("Shed").state["notice_text"] = str(_take_result.get("text", ""))
        $ rooms.get("Shed").state["notice_pending"] = True
    $ scene_runtime.text = str(_take_result.get("text", "") or "Здесь уже нечего брать.")
    if _current_room_code == "Shed":
        $ scene_runtime.text = build_shed_description(True, "")
        $ main_ui_runtime.action_items = build_shed_action_items()
    elif _current_room_code == "TavernMyRoom":
        $ main_ui_runtime.action_items = tavern_my_room_action_items()
    $ scene_runtime.location_text = scene_runtime.text
    call stat
    $ renpy.restart_interaction()
    return


label Drop(what_id="", where_id="", fallback_text="", object_id=""):
    $ renpy.dynamic("item_id", "_drop_room_code", "_drop_result")
    $ item_id = str(what_id or "").strip()
    $ _drop_room_code = str(where_id or getattr(rooms.current, "code_name", "") or rooms.current_code or "").strip()
    if item_id == "" or get_game_item(item_id) is None:
        $ scene_runtime.text = "Непонятно, что именно вы пытаетесь оставить."
        $ scene_runtime.location_text = scene_runtime.text
        return

    $ _drop_result = player_drop_item(rooms.current, item_id)
    if _drop_result.get("ok", False):
        if _drop_room_code == "Shed" and item_id == "lumber_001":
            $ _pc_register_chore_success("bring_woods")
        $ scene_runtime.text = str(fallback_text or _drop_result.get("text", "Вы оставляете предмет здесь.") or "Вы оставляете предмет здесь.")
    else:
        $ scene_runtime.text = str(_drop_result.get("text", "У вас этого нет.") or "У вас этого нет.")

    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    return


label Drink(what_id="", where_id="", fallback_text="", object_id=""):
    $ renpy.dynamic("_drink_result")
    $ _drink_result = player_use_item(what_id, "drink", False)
    $ scene_runtime.text = str(_drink_result.get("text", fallback_text) or fallback_text or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    return


label UseDrinkItem(what_id=""):
    $ renpy.dynamic("_drink_item_id", "_drink_result")
    $ _drink_item_id = str(what_id or "").strip()
    $ _drink_result = player_use_item(_drink_item_id, "drink", True)
    $ scene_runtime.text = str(_drink_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    $ player_card_show_inventory_menu_state(True)
    return


label EatItem(what_id="", where_id="", fallback_text="", object_id=""):
    $ renpy.dynamic("_eat_item_result")
    $ _eat_item_result = player_use_item(what_id, "eat", False)
    $ scene_runtime.text = str(_eat_item_result.get("text", fallback_text) or fallback_text or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    return


label Eat(item_name="", item_energy=0, fallback_text="", where_id="", object_id=""):
    $ renpy.dynamic("_eat_result")
    $ _eat_result = player_eat_meal(item_name, item_energy)
    $ scene_runtime.text = str(_eat_result.get("text", fallback_text) or fallback_text or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    return


label UseFoodItem(what_id=""):
    $ renpy.dynamic("_food_item_id", "_food_result")
    $ _food_item_id = str(what_id or "").strip()
    $ _food_result = player_use_item(_food_item_id, "eat", True)
    $ scene_runtime.text = str(_food_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    $ player_card_show_inventory_item_state(_food_item_id, True)
    return


label Wash(what_id="", where_id="", fallback_text="", object_id=""):
    $ renpy.dynamic("_wash_block", "_wash_result")
    $ _wash_block = action_restriction_result("wash", "wash")
    if not _wash_block.get("ok", False):
        $ scene_runtime.text = str(_wash_block.get("text", fallback_text) or fallback_text or "")
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ _wash_result = player_wash_with_rainwater()
    $ scene_runtime.text = str(_wash_result.get("text", fallback_text) or fallback_text or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    return


label DoChore(chore_key="", where_id="", fallback_text="", object_id=""):
    $ renpy.dynamic("_chore_block", "_chore_key", "_chore_result")
    $ _chore_block = action_restriction_result("chore", "do_chore")
    if not _chore_block.get("ok", False):
        $ scene_runtime.text = str(_chore_block.get("text", fallback_text) or fallback_text or "")
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ _chore_key = str(chore_key or "").strip()
    $ _chore_result = do_player_chore(_chore_key, where_id, object_id)
    $ scene_runtime.text = str(_chore_result.get("text", fallback_text) or fallback_text or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ update_stat_state()
    return


label Sleep(return_location="TavernMain", timepassed=1, fallback_text="", where_id="", object_id=""):
    $ renpy.dynamic("_sleep_target", "_sleep_days", "_sleep_where", "_sleep_object")
    $ _sleep_target = str(return_location or "TavernMain")
    $ _sleep_days = max(1, int(timepassed or 1))
    $ _sleep_where = str(where_id or rooms.current_code or _sleep_target or "TavernMain")
    $ _sleep_object = str(object_id or main_ui_runtime.object_id or "")
    if not _player_can_sleep_now():
        $ scene_runtime.text = "Еще слишком рано ложиться спать."
        $ scene_runtime.location_text = scene_runtime.text
        return
    if str(fallback_text or "").strip() != "":
        $ scene_runtime.text = str(fallback_text or "").strip()
        $ scene_runtime.location_text = scene_runtime.text
    if melissa_night_wake_event_ready(_sleep_target):
        call MelissaNightWakeEvent
    call NextDay(_sleep_target, _sleep_days)
    if renpy.has_label(_sleep_target):
        jump expression _sleep_target
    return 


label Rest(return_location="", minutes_passed=120, energy_gain=15, fallback_text="", where_id="", object_id=""):
    $ renpy.dynamic("_rest_text", "_rest_block", "_rest_target", "_rest_minutes", "_rest_energy")
    $ _rest_block = action_restriction_result("rest", "rest")
    if not _rest_block.get("ok", False):
        $ scene_runtime.text = str(_rest_block.get("text", fallback_text) or fallback_text or "")
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ _rest_target = str(return_location or rooms.current_code or "TavernMyRoom")
    $ _rest_minutes = max(0, int(minutes_passed or 0))
    $ _rest_energy = int(energy_gain or 0)
    $ _rest_text = str(fallback_text or "").strip()
    if _rest_text:
        $ _rest_text = _rest_text + " You feel rested and refreshed!"
    else:
        $ _rest_text = "You feel rested and refreshed!"
    if _rest_minutes > 0:
        $ calendar_v2.advance_minutes(_rest_minutes)
    $ update_stat_state()
    $ player.change_stat("energy", _rest_energy)
    $ scene_runtime.text = _rest_text
    $ scene_runtime.location_text = scene_runtime.text
    return


label MakeFire(what_id="", where_id="", fallback_text="", object_id=""):
    $ renpy.dynamic("_fire_result")
    $ _fire_result = do_player_chore("make_fire", where_id, object_id or what_id)
    $ scene_runtime.text = str(_fire_result.get("text", fallback_text) or fallback_text or "")
    $ scene_runtime.location_text = scene_runtime.text
    return


label Clean(what_id="", where_id="", fallback_text="", object_id=""):
    $ renpy.dynamic("_clean_block", "_clean_result")
    $ _clean_block = action_restriction_result("chore", "clean")
    if not _clean_block.get("ok", False):
        $ scene_runtime.text = str(_clean_block.get("text", fallback_text) or fallback_text or "")
        $ scene_runtime.location_text = scene_runtime.text
        return
    if str(what_id or "") == "ashes":
        $ _clean_result = do_player_chore("clean_ashes", where_id, object_id or what_id)
        $ scene_runtime.text = str(_clean_result.get("text", fallback_text) or fallback_text or "")
        $ scene_runtime.location_text = scene_runtime.text
    else:
        $ scene_runtime.text = str(fallback_text or "Сейчас это нельзя почистить.")
        $ scene_runtime.location_text = scene_runtime.text
    return


label BoilWater(what_id="", where_id="", fallback_text="", object_id=""):
    $ renpy.dynamic("_boil_block", "_boil_result")
    $ _boil_block = action_restriction_result("chore", "boil_water")
    if not _boil_block.get("ok", False):
        $ scene_runtime.text = str(_boil_block.get("text", fallback_text) or fallback_text or "")
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ _boil_result = do_player_chore("boil_water", where_id, object_id or what_id)
    $ scene_runtime.text = str(_boil_result.get("text", fallback_text) or fallback_text or "")
    $ scene_runtime.location_text = scene_runtime.text
    return
