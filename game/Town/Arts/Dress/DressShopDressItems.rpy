# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def dress_shop_item_code(item_obj):
        if item_obj is None:
            return ""
        if isinstance(getattr(item_obj, "custom_properties", None), dict):
            return str(item_obj.custom_properties.get("dress_code", "") or "")
        return str(getattr(item_obj, "code_name", "") or "")

    def dress_shop_item_depreciated(item_obj):
        dress_code = dress_shop_item_code(item_obj)
        if not dress_code:
            return False
        if not player_state().appearance.has_dress(dress_code):
            return False
        if "player_current_dress_age_days" not in globals() or "player_dress_condition_from_age" not in globals():
            return False
        return int(player_dress_condition_from_age(player_current_dress_age_days(dress_code)) or 0) <= 0

    def dress_shop_can_buy_item(item_obj):
        dress_code = dress_shop_item_code(item_obj)
        item_price = int(getattr(item_obj, "price", 0) or 0)
        if str(DressProduced or "") != "":
            return False
        if not bool(dress_code) or item_price > int(money or 0):
            return False
        return not player_state().appearance.has_dress(dress_code) or dress_shop_item_depreciated(item_obj)

    def dress_shop_item_owned(item_obj):
        dress_code = dress_shop_item_code(item_obj)
        return bool(dress_code) and player_state().appearance.has_dress(dress_code) and not dress_shop_item_depreciated(item_obj)

    def dress_shop_prepare_dress_item(dress_code, female_rack=False):
        dress_id = str(dress_code or "").strip()
        if not dress_id:
            return None

        item_obj = get_game_item("dress_" + dress_id)
        if item_obj is None:
            return None

        actions = []
        if female_rack:
            actions.append(
                ObjectAction(
                    action_id="female_dress_info_" + dress_id,
                    label="Спросить Ирму о платье",
                    hook="text",
                    target="Ирма говорит, что это " + str(getattr(item_obj, "name", dress_id) or dress_id).lower() + ", и обойдется оно в " + str(int(getattr(item_obj, "price", 0) or 0)) + " мараведи.",
                )
            )
        else:
            actions.append(
                ObjectAction(
                    action_id="buy_male_dress_" + dress_id,
                    label="Купить для себя",
                    hook="call",
                    target="DressShopBuyMaleItem",
                    args=(dress_id,),
                    condition=dress_shop_can_buy_item,
                )
            )
            actions.append(
                ObjectAction(
                    action_id="owned_male_dress_" + dress_id,
                    label="Уже куплено",
                    hook="text",
                    target="Этот костюм уже лежит среди вашей одежды.",
                    condition=dress_shop_item_owned,
                )
            )

        item_obj.actions = actions
        item_obj.custom_properties["female_rack"] = bool(female_rack)
        item_obj.custom_properties["wear_target"] = "female" if female_rack else "player"
        return item_obj

    def dress_shop_rack_items(rack_type):
        if "ensure_game_item_registry" in globals():
            ensure_game_item_registry()
        items = []
        if str(rack_type or "") == "female":
            for item_id in list(womenDress or []):
                item_obj = get_game_item(item_id)
                code = dress_shop_item_code(item_obj)
                if not item_obj or not code or code == "nightshirt":
                    continue
                dress_item = dress_shop_prepare_dress_item(code, True)
                if dress_item is not None:
                    items.append(dress_item)
        else:
            for item_id in list(menDress or []):
                item_obj = get_game_item(item_id)
                code = dress_shop_item_code(item_obj)
                if not code:
                    continue
                dress_item = dress_shop_prepare_dress_item(code, False)
                if dress_item is not None:
                    items.append(dress_item)
        return items
