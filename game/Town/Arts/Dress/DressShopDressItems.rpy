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
        if not player.appearance.has_dress(dress_code):
            return False
        return int(player.appearance.dress_condition(dress_code) or 0) <= 0

    def dress_shop_can_buy_item(item_obj):
        dress_code = dress_shop_item_code(item_obj)
        item_price = int(getattr(item_obj, "price", 0) or 0)
        if str(dress_shop.produced or "") != "":
            return False
        if not bool(dress_code) or item_price > int(player.economy.money or 0):
            return False
        return not player.appearance.has_dress(dress_code) or dress_shop_item_depreciated(item_obj)

    def dress_shop_item_owned(item_obj):
        dress_code = dress_shop_item_code(item_obj)
        return bool(dress_code) and player.appearance.has_dress(dress_code) and not dress_shop_item_depreciated(item_obj)

    def dress_shop_rack_items(rack_type):
        items = []
        if str(rack_type or "") == "female":
            for item_id in FEMALE_DRESS_ITEM_IDS:
                item_obj = get_game_item(item_id)
                code = dress_shop_item_code(item_obj)
                if not item_obj or not code or code == "nightshirt":
                    continue
                items.append(item_obj)
        else:
            for item_id in MALE_DRESS_ITEM_IDS:
                item_obj = get_game_item(item_id)
                code = dress_shop_item_code(item_obj)
                if not code:
                    continue
                items.append(item_obj)
        return items
