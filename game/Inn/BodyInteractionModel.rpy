default BodyInteractionProfiles = {}

init python:
    BODYMODEL_PARTS = ("head", "upper", "pelvis", "lower", "feet", "hands", "palms")
    BODYMODEL_LAYERS = ("layer_0", "layer_1", "layer_2")
    BODYMODEL_UNIVERSAL_ACTIONS = ("fondle", "touch", "caress", "kiss", "suck", "lick", "insert", "pinch", "open", "spread")
    BODYMODEL_CONTAINER_IDS = ("mouth", "pussy", "ass")
    BODYMODEL_EROGENOUS_TARGETS = ("mouth", "pussy", "ass", "nipples")
    BODYMODEL_PART_LABELS = {
        "head": "Голова",
        "upper": "Верх",
        "pelvis": "Таз",
        "lower": "Ноги",
        "feet": "Ступни",
        "hands": "Кисти",
        "palms": "Ладони",
    }
    BODYMODEL_LAYER_LABELS = {
        "layer_0": "Слой 0",
        "layer_1": "Слой 1",
        "layer_2": "Слой 2",
    }

    BODYMODEL_ITEM_COVERAGE = {
        "simplebra": {"upper": "layer_0"},
        "simplepanties": {"pelvis": "layer_0"},
        "whitestockings": {"lower": "layer_0"},
        "blackstockings": {"lower": "layer_0"},
        "redstockings": {"lower": "layer_0"},
        "simpleshoes": {"feet": "layer_1"},
        "highshoes": {"feet": "layer_1"},
        "woodenslippers": {"feet": "layer_1"},
        "modestworkdress": {"upper": "layer_1", "pelvis": "layer_1"},
        "modestnicedress": {"upper": "layer_1", "pelvis": "layer_1"},
        "workdress": {"upper": "layer_1", "pelvis": "layer_1"},
        "workdresszhilet": {"upper": "layer_1", "pelvis": "layer_1"},
        "greenworkdress": {"upper": "layer_1", "pelvis": "layer_1"},
        "openworkdress": {"upper": "layer_1", "pelvis": "layer_1"},
        "minidress": {"upper": "layer_1", "pelvis": "layer_1"},
        "slutdress": {"upper": "layer_1", "pelvis": "layer_1"},
        "nightshirt": {"upper": "layer_1", "pelvis": "layer_1"},
        "bluemodestblouse": {"upper": "layer_1"},
        "whiteniceblouse": {"upper": "layer_1"},
        "whiteworksemiopenblouse": {"upper": "layer_1"},
        "whiteworkblousezhilet": {"upper": "layer_1"},
        "greenworksemiopenblouse": {"upper": "layer_1"},
        "dekolteblouse": {"upper": "layer_1"},
        "lightblouse": {"upper": "layer_1"},
        "transparentblouse": {"upper": "layer_1"},
        "nightshirttop": {"upper": "layer_1"},
        "bluelongskirt": {"pelvis": "layer_1"},
        "whiteniceLongskirt": {"pelvis": "layer_1"},
        "brownlongskirt": {"pelvis": "layer_1"},
        "brownmidiskirt": {"pelvis": "layer_1"},
        "miniskirt": {"pelvis": "layer_1"},
        "ultraminiskirt": {"pelvis": "layer_1"},
        "nightshirtbottom": {"pelvis": "layer_1"},
    }
    BODYMODEL_ITEM_META = {
        "simplebra": {"name": "лиф", "liftable": False, "removable": True},
        "simplepanties": {"name": "панталончики", "liftable": False, "removable": True, "kind": "panties"},
        "whitestockings": {"name": "белые чулки", "liftable": False, "removable": True},
        "blackstockings": {"name": "черные чулки", "liftable": False, "removable": True},
        "redstockings": {"name": "красные чулки", "liftable": False, "removable": True},
        "simpleshoes": {"name": "простые туфли", "liftable": False, "removable": True},
        "highshoes": {"name": "высокие туфли", "liftable": False, "removable": True},
        "woodenslippers": {"name": "деревянные шлепанцы", "liftable": False, "removable": True},
        "bluemodestblouse": {"name": "скромная блуза", "liftable": True, "removable": True},
        "whiteniceblouse": {"name": "нарядная блуза", "liftable": True, "removable": True},
        "whiteworksemiopenblouse": {"name": "рабочая блузка", "liftable": True, "removable": True},
        "whiteworkblousezhilet": {"name": "блузка с жилеткой", "liftable": True, "removable": True},
        "greenworksemiopenblouse": {"name": "зеленая блузка", "liftable": True, "removable": True},
        "dekolteblouse": {"name": "блузка с декольте", "liftable": True, "removable": True},
        "lightblouse": {"name": "легкая блузка", "liftable": True, "removable": True},
        "transparentblouse": {"name": "прозрачная блузка", "liftable": True, "removable": True},
        "nightshirttop": {"name": "верх ночной рубашки", "liftable": True, "removable": True},
        "bluelongskirt": {"name": "длинная юбка", "liftable": True, "removable": True, "kind": "skirt"},
        "whiteniceLongskirt": {"name": "нарядная длинная юбка", "liftable": True, "removable": True, "kind": "skirt"},
        "brownlongskirt": {"name": "длинная юбка", "liftable": True, "removable": True, "kind": "skirt"},
        "brownmidiskirt": {"name": "юбка ниже колен", "liftable": True, "removable": True, "kind": "skirt"},
        "miniskirt": {"name": "мини-юбка", "liftable": True, "removable": True, "kind": "skirt"},
        "ultraminiskirt": {"name": "ультрамини-юбка", "liftable": True, "removable": True, "kind": "skirt"},
        "nightshirtbottom": {"name": "низ ночной рубашки", "liftable": True, "removable": True},
    }

    def bodymodel_blank_slot():
        return {"item_id": "", "state": "none"}

    def bodymodel_blank_part():
        return {layer_name: bodymodel_blank_slot() for layer_name in BODYMODEL_LAYERS}

    def bodymodel_blank_access():
        return {action_id: False for action_id in BODYMODEL_UNIVERSAL_ACTIONS}

    def bodymodel_blank_containers():
        return {
            container_id: {"state": "dry", "wetness": 0, "itch": 0}
            for container_id in BODYMODEL_CONTAINER_IDS
        }

    def bodymodel_blank_features():
        return {
            "nipples": "soft",
            "dick_erection": 0,
            "dick_description": "",
        }

    def bodymodel_blank_target_access():
        return {
            target_id: bodymodel_blank_access()
            for target_id in BODYMODEL_EROGENOUS_TARGETS
        }

    def bodymodel_container_state_name(wetness=0, itch=0):
        wet_value = int(wetness or 0)
        itch_value = int(itch or 0)
        if wet_value >= 70:
            return "slurping"
        if itch_value > 0 and wet_value > 0:
            return "itchy and wet"
        if itch_value > 0:
            return "itchy"
        if wet_value > 0:
            return "wet"
        return "dry"

    def bodymodel_blank_profile(char_id="", display_name="", body_type="female"):
        profile_id = str(char_id or "").strip()
        return {
            "id": profile_id,
            "display_name": str(display_name or profile_id),
            "body_type": str(body_type or "female"),
            "parts": {part_name: bodymodel_blank_part() for part_name in BODYMODEL_PARTS},
            "containers": bodymodel_blank_containers(),
            "features": bodymodel_blank_features(),
            "arousal": 0,
            "orgasm_threshold": 100,
            "naked": True,
            "access": bodymodel_blank_target_access(),
        }

    def bodymodel_register_character(char_id="", display_name="", body_type="female"):
        profile_id = str(char_id or "").strip()
        if not profile_id:
            return {}
        profile = dict(BodyInteractionProfiles.get(profile_id, {}) or {})
        if not profile:
            profile = bodymodel_blank_profile(profile_id, display_name, body_type)
        else:
            profile.setdefault("id", profile_id)
            profile["display_name"] = str(display_name or profile.get("display_name", profile_id) or profile_id)
            profile["body_type"] = str(body_type or profile.get("body_type", "female") or "female")
            profile.setdefault("parts", {part_name: bodymodel_blank_part() for part_name in BODYMODEL_PARTS})
            profile.setdefault("containers", bodymodel_blank_containers())
            profile.setdefault("features", bodymodel_blank_features())
            profile.setdefault("access", bodymodel_blank_target_access())
        BodyInteractionProfiles[profile_id] = profile
        return profile

    def bodymodel_clear_clothing(profile):
        if not isinstance(profile, dict):
            return
        profile["parts"] = {part_name: bodymodel_blank_part() for part_name in BODYMODEL_PARTS}

    def bodymodel_set_item(profile, item_id="", state="worn"):
        if not isinstance(profile, dict):
            return
        item_key = str(item_id or "").strip()
        if not item_key:
            return
        state_key = str(state or "worn").strip() or "worn"
        coverage = dict(BODYMODEL_ITEM_COVERAGE.get(item_key, {}) or {})
        for part_name, layer_name in coverage.items():
            if part_name not in BODYMODEL_PARTS or layer_name not in BODYMODEL_LAYERS:
                continue
            profile["parts"].setdefault(part_name, bodymodel_blank_part())
            profile["parts"][part_name][layer_name] = {
                "item_id": item_key,
                "state": state_key,
            }

    def bodymodel_slot_item(profile, part_name="", layer_name=""):
        if not isinstance(profile, dict):
            return {}
        return dict(profile.get("parts", {}).get(str(part_name or ""), {}).get(str(layer_name or ""), {}) or {})

    def bodymodel_slot_blocks(profile, part_name="", layer_name=""):
        slot = bodymodel_slot_item(profile, part_name, layer_name)
        return bool(str(slot.get("item_id", "") or "").strip()) and str(slot.get("state", "none") or "none") == "worn"

    def bodymodel_target_parts(target_id=""):
        target_key = str(target_id or "").strip()
        if target_key == "nipples":
            return ("upper",)
        if target_key in ("pussy", "ass"):
            return ("pelvis",)
        return ()

    def bodymodel_target_block_state(profile, target_id=""):
        part_names = tuple(bodymodel_target_parts(target_id))
        if len(part_names) <= 0:
            outer_block = False
            inner_block = False
        else:
            outer_block = any(
                bodymodel_slot_blocks(profile, part_name, "layer_1") or bodymodel_slot_blocks(profile, part_name, "layer_2")
                for part_name in part_names
            )
            inner_block = any(bodymodel_slot_blocks(profile, part_name, "layer_0") for part_name in part_names)
        return {
            "outer": bool(outer_block),
            "inner": bool(inner_block),
            "level": 2 if outer_block else 1 if inner_block else 0,
        }

    def bodymodel_update_container_states(profile):
        if not isinstance(profile, dict):
            return
        containers = profile.setdefault("containers", {})
        for container_id in BODYMODEL_CONTAINER_IDS:
            container_state = containers.setdefault(container_id, {"state": "dry", "wetness": 0, "itch": 0})
            container_state["state"] = bodymodel_container_state_name(
                container_state.get("wetness", 0),
                container_state.get("itch", 0),
            )

    def bodymodel_compute_access(profile):
        if not isinstance(profile, dict):
            return

        upper_outer = bodymodel_slot_blocks(profile, "upper", "layer_1") or bodymodel_slot_blocks(profile, "upper", "layer_2")
        upper_inner = bodymodel_slot_blocks(profile, "upper", "layer_0")
        pelvis_outer = bodymodel_slot_blocks(profile, "pelvis", "layer_1") or bodymodel_slot_blocks(profile, "pelvis", "layer_2")
        pelvis_inner = bodymodel_slot_blocks(profile, "pelvis", "layer_0")

        mouth_access = bodymodel_blank_access()
        for action_id in ("fondle", "touch", "caress", "kiss", "suck", "lick", "insert", "open", "spread"):
            mouth_access[action_id] = True
        mouth_access["pinch"] = False

        nipple_access = bodymodel_blank_access()
        if not upper_outer:
            for action_id in ("fondle", "touch", "caress", "pinch"):
                nipple_access[action_id] = True
        if not upper_outer and not upper_inner:
            for action_id in ("kiss", "suck", "lick"):
                nipple_access[action_id] = True

        pussy_access = bodymodel_blank_access()
        ass_access = bodymodel_blank_access()

        if pelvis_outer:
            for action_id in ("fondle", "touch", "caress"):
                pussy_access[action_id] = True
                ass_access[action_id] = True
        elif pelvis_inner:
            for action_id in ("fondle", "touch", "caress", "pinch"):
                pussy_access[action_id] = True
                ass_access[action_id] = True
        else:
            for action_id in ("fondle", "touch", "caress", "kiss", "lick", "insert", "pinch", "open", "spread"):
                pussy_access[action_id] = True
                ass_access[action_id] = True

        profile["access"] = {
            "mouth": mouth_access,
            "pussy": pussy_access,
            "ass": ass_access,
            "nipples": nipple_access,
        }

        profile["naked"] = True
        for part_name in BODYMODEL_PARTS:
            for layer_name in BODYMODEL_LAYERS:
                slot = bodymodel_slot_item(profile, part_name, layer_name)
                if str(slot.get("item_id", "") or "").strip():
                    profile["naked"] = False
                    return

    def bodymodel_sync_character(char_id="", display_name="", body_type="female"):
        profile_id = str(char_id or "").strip()
        if not profile_id:
            return {}

        resolved_name = str(display_name or RealName.get(profile_id, profile_id) or profile_id)
        profile = bodymodel_register_character(profile_id, resolved_name, body_type)
        bodymodel_clear_clothing(profile)

        top_item = str(topdress.get(profile_id, "") or topdressdef.get(profile_id, "") or DressTopPart.get(dressdefault.get(profile_id, ""), "") or "")
        bottom_item = str(bottomdress.get(profile_id, "") or bottomdressdef.get(profile_id, "") or DressBottomPart.get(dressdefault.get(profile_id, ""), "") or "")
        bra_item = str(bra.get(profile_id, "") or bradef.get(profile_id, "") or "")
        panties_item = str(panties.get(profile_id, "") or pantiesdef.get(profile_id, "") or "")
        legs_item = str(legs.get(profile_id, "") or legsdef.get(profile_id, "") or "")
        shoes_item = str(shoes.get(profile_id, "") or shoesdef.get(profile_id, "") or "")

        bodymodel_set_item(profile, top_item, "lifted" if int(topraised.get(profile_id, 0) or 0) == 1 else "worn")
        bodymodel_set_item(profile, bottom_item, "lifted" if int(bottomraised.get(profile_id, 0) or 0) == 1 else "worn")
        bodymodel_set_item(profile, bra_item, "worn")
        bodymodel_set_item(profile, panties_item, "worn")
        bodymodel_set_item(profile, legs_item, "worn")
        bodymodel_set_item(profile, shoes_item, "worn")

        bodymodel_update_container_states(profile)
        bodymodel_compute_access(profile)
        BodyInteractionProfiles[profile_id] = profile
        return profile

    def bodymodel_actions_for_target(char_id="", target_id=""):
        profile = BodyInteractionProfiles.get(str(char_id or "").strip(), {}) or {}
        access = dict(profile.get("access", {}).get(str(target_id or ""), {}) or {})
        return [action_id for action_id in BODYMODEL_UNIVERSAL_ACTIONS if bool(access.get(action_id, False))]

    def bodymodel_item_meta(item_id=""):
        return dict(BODYMODEL_ITEM_META.get(str(item_id or "").strip(), {}) or {})

    def bodymodel_item_name(item_id=""):
        item_key = str(item_id or "").strip()
        if not item_key:
            return ""
        meta = bodymodel_item_meta(item_key)
        if str(meta.get("name", "") or "").strip():
            return str(meta.get("name", "") or "")
        short_names = globals().get("ShortDressName", {}) or {}
        return str(short_names.get(item_key, item_key) or item_key)

    def bodymodel_sync_profile_arousal(profile, char_id=""):
        if not isinstance(profile, dict):
            return {}
        key = str(char_id or profile.get("id", "") or "").strip()
        if key and isinstance(Arousal, dict):
            profile["arousal"] = int(Arousal.get(key, Arousal.get("You" if key.lower() == "you" else key, profile.get("arousal", 0))) or 0)
        arousal_value = int(profile.get("arousal", 0) or 0)
        if arousal_value >= 70:
            profile.setdefault("features", {})["nipples"] = "swallowed"
        elif arousal_value >= 30:
            profile.setdefault("features", {})["nipples"] = "erected"
        else:
            profile.setdefault("features", {})["nipples"] = "soft"
        profile.setdefault("features", {})["dick_erection"] = 0 if arousal_value < 20 else 1 if arousal_value < 65 else 2 if arousal_value < 100 else 3
        if profile["features"]["dick_erection"] <= 0:
            profile["features"]["dick_description"] = "вялый"
        elif profile["features"]["dick_erection"] == 1:
            profile["features"]["dick_description"] = "поднимается"
        elif profile["features"]["dick_erection"] == 2:
            profile["features"]["dick_description"] = "крепко стоит"
        else:
            profile["features"]["dick_description"] = "пульсирует на грани разрядки"
        bodymodel_update_container_states(profile)
        return profile

    def bodymodel_profile_summary_text(profile):
        if not isinstance(profile, dict):
            return ""
        bodymodel_sync_profile_arousal(profile, profile.get("id", ""))
        lines = []
        display_name = str(profile.get("display_name", profile.get("id", "")) or "")
        if bool(profile.get("naked", False)):
            lines.append("%s сейчас полностью раздет%s." % (display_name, "а" if str(profile.get("body_type", "female")) == "female" else ""))
        else:
            for part_name in BODYMODEL_PARTS:
                part_slots = []
                for layer_name in BODYMODEL_LAYERS:
                    slot = bodymodel_slot_item(profile, part_name, layer_name)
                    item_name = bodymodel_item_name(slot.get("item_id", ""))
                    if not item_name:
                        continue
                    state_name = str(slot.get("state", "worn") or "worn")
                    if state_name == "lifted":
                        item_name = item_name + " (приподнято)"
                    part_slots.append("%s: %s" % (BODYMODEL_LAYER_LABELS.get(layer_name, layer_name), item_name))
                if part_slots:
                    lines.append("%s: %s." % (BODYMODEL_PART_LABELS.get(part_name, part_name), ", ".join(part_slots)))
        lines.append("Соски: %s." % str(profile.get("features", {}).get("nipples", "soft") or "soft"))
        lines.append("Рот: %s." % str(profile.get("containers", {}).get("mouth", {}).get("state", "dry") or "dry"))
        lines.append("Киска: %s." % str(profile.get("containers", {}).get("pussy", {}).get("state", "dry") or "dry"))
        lines.append("Попка: %s." % str(profile.get("containers", {}).get("ass", {}).get("state", "dry") or "dry"))
        return "\n".join([row for row in lines if str(row or "").strip() != ""])

    def bodymodel_action_effect(profile, target_id="", action_id=""):
        target_key = str(target_id or "").strip()
        action_key = str(action_id or "").strip()
        access = dict(profile.get("access", {}).get(target_key, {}) or {})
        block_state = bodymodel_target_block_state(profile, target_key)
        base_target = {
            "mouth": {"kiss": 8, "lick": 10, "suck": 12, "insert": 14, "caress": 4, "touch": 4, "fondle": 3, "open": 3, "spread": 2},
            "nipples": {"fondle": 8, "touch": 6, "caress": 7, "kiss": 10, "lick": 12, "suck": 14, "pinch": 9},
            "pussy": {"fondle": 8, "touch": 6, "caress": 7, "kiss": 10, "lick": 14, "insert": 18, "pinch": 7, "open": 4, "spread": 5},
            "ass": {"fondle": 6, "touch": 5, "caress": 6, "lick": 10, "insert": 13, "pinch": 6, "open": 4, "spread": 5},
        }
        base_actor = {
            "mouth": {"kiss": 6, "lick": 6, "suck": 10, "insert": 14, "caress": 2, "touch": 2, "fondle": 2},
            "nipples": {"fondle": 6, "touch": 4, "caress": 5, "kiss": 7, "lick": 9, "suck": 10, "pinch": 4},
            "pussy": {"fondle": 7, "touch": 6, "caress": 6, "kiss": 9, "lick": 12, "insert": 16, "pinch": 5, "open": 2, "spread": 2},
            "ass": {"fondle": 5, "touch": 4, "caress": 4, "lick": 8, "insert": 10, "pinch": 4, "open": 2, "spread": 2},
        }
        wetness_gain = {
            "mouth": {"kiss": 3, "lick": 5, "suck": 6, "insert": 6},
            "pussy": {"fondle": 4, "touch": 3, "caress": 4, "kiss": 5, "lick": 8, "insert": 10, "open": 2, "spread": 2},
            "ass": {"lick": 4, "insert": 5, "open": 1, "spread": 1},
        }
        if not bool(access.get(action_key, False)):
            return {
                "allowed": False,
                "target": target_key,
                "action": action_key,
                "block_state": block_state,
                "target_gain": 0,
                "actor_gain": 0,
                "wetness_gain": 0,
            }
        coefficient = 1.0
        if block_state.get("level", 0) == 1:
            coefficient = 0.65
        elif block_state.get("level", 0) >= 2:
            coefficient = 0.45
        target_gain = int(round(float(base_target.get(target_key, {}).get(action_key, 4) or 0) * coefficient))
        actor_gain = int(round(float(base_actor.get(target_key, {}).get(action_key, 3) or 0) * max(0.5, coefficient)))
        container_gain = int(round(float(wetness_gain.get(target_key, {}).get(action_key, 0) or 0) * coefficient))
        return {
            "allowed": True,
            "target": target_key,
            "action": action_key,
            "block_state": block_state,
            "target_gain": max(0, target_gain),
            "actor_gain": max(0, actor_gain),
            "wetness_gain": max(0, container_gain),
        }

    def bodymodel_apply_action(char_id="", target_id="", action_id="", actor_id="You", display_name="", body_type="female"):
        profile_id = str(char_id or "").strip()
        actor_key = str(actor_id or "").strip() or "You"
        if not profile_id:
            return {"allowed": False, "target": str(target_id or ""), "action": str(action_id or "")}
        profile = bodymodel_sync_character(profile_id, display_name, body_type)
        bodymodel_sync_profile_arousal(profile, profile_id)
        effect = bodymodel_action_effect(profile, target_id, action_id)
        if not bool(effect.get("allowed", False)):
            effect["profile"] = profile
            effect["arousal"] = int(profile.get("arousal", 0) or 0)
            effect["container_state"] = str(profile.get("containers", {}).get(str(target_id or ""), {}).get("state", "") or "")
            return effect
        if isinstance(Arousal, dict):
            Arousal[profile_id] = min(100, max(0, int(Arousal.get(profile_id, profile.get("arousal", 0)) or 0) + int(effect.get("target_gain", 0) or 0)))
            if actor_key.lower() == "you":
                Arousal["You"] = min(100, max(0, int(Arousal.get("You", 0) or 0) + int(effect.get("actor_gain", 0) or 0)))
                Arousal["you"] = Arousal["You"]
            else:
                Arousal[actor_key] = min(100, max(0, int(Arousal.get(actor_key, 0) or 0) + int(effect.get("actor_gain", 0) or 0)))
        container_key = str(target_id or "").strip()
        if container_key in ("mouth", "pussy", "ass"):
            container_state = profile.setdefault("containers", {}).setdefault(container_key, {"state": "dry", "wetness": 0, "itch": 0})
            container_state["wetness"] = min(100, max(0, int(container_state.get("wetness", 0) or 0) + int(effect.get("wetness_gain", 0) or 0)))
            container_state["state"] = bodymodel_container_state_name(container_state.get("wetness", 0), container_state.get("itch", 0))
        profile["arousal"] = int(Arousal.get(profile_id, profile.get("arousal", 0)) or 0)
        bodymodel_sync_profile_arousal(profile, profile_id)
        BodyInteractionProfiles[profile_id] = profile
        effect["profile"] = profile
        effect["arousal"] = int(profile.get("arousal", 0) or 0)
        effect["container_state"] = str(profile.get("containers", {}).get(container_key, {}).get("state", "") or "")
        effect["orgasm"] = int(profile.get("arousal", 0) or 0) >= int(profile.get("orgasm_threshold", 100) or 100)
        return effect
