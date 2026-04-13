init python:
    def dress_shop_item_code(item_obj):
        if item_obj is None:
            return ""
        if isinstance(getattr(item_obj, "custom_properties", None), dict):
            return str(item_obj.custom_properties.get("dress_code", "") or "")
        return str(getattr(item_obj, "code_name", "") or "")

    def dress_shop_can_buy_item(item_obj):
        dress_code = dress_shop_item_code(item_obj)
        item_price = int(getattr(item_obj, "price", 0) or 0)
        return bool(dress_code) and item_price <= int(money or 0) and dress_code not in list(MyDresses or [])

    def dress_shop_item_owned(item_obj):
        dress_code = dress_shop_item_code(item_obj)
        return bool(dress_code) and dress_code in list(MyDresses or [])

    def dress_shop_build_dress_item(dress_code, female_rack=False):
        dress_id = str(dress_code or "").strip()
        if not dress_id:
            return None

        short_name = str(_gds_get_dict("ShortDressName").get(dress_id, dress_id)).strip()
        full_desc = str(_gds_get_dict("FullDressDesc").get(dress_id, dress_id)).strip()
        price = _gds_dress_cost(dress_id)

        actions = []
        if female_rack:
            actions.append(
                ObjectAction(
                    action_id="female_dress_info_" + dress_id,
                    label="Спросить Ирму о платье",
                    hook="text",
                    target="Ирма говорит, что это " + short_name.lower() + ", и обойдется оно в " + str(price) + " мараведи.",
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

        return GameObject(
            object_id="dress_" + dress_id,
            name=short_name,
            description=full_desc,
            actions=actions,
            picture="",
            price=price,
            carriable=True,
            wearable=True,
            stackable=False,
            custom_properties={
                "dress_code": dress_id,
                "female_rack": bool(female_rack),
                "wear_target": "female" if female_rack else "player",
            },
        )

    def dress_shop_rack_items(rack_type):
        items = []
        if str(rack_type or "") == "female":
            for dress_code in list(_gds_get_list("FemaleDressCodes")):
                code = str(dress_code or "").strip()
                if not code or code == "nightshirt":
                    continue
                dress_item = dress_shop_build_dress_item(code, True)
                if dress_item is not None:
                    items.append(dress_item)
        else:
            for dress_code in list(_gds_get_list("MaleDressCodes")):
                code = str(dress_code or "").strip()
                if not code:
                    continue
                dress_item = dress_shop_build_dress_item(code, False)
                if dress_item is not None:
                    items.append(dress_item)
        return items

    def dress_shop_get_item(item_id, female_rack=False):
        target_id = str(item_id or "").strip()
        for dress_item in dress_shop_rack_items("female" if female_rack else "male"):
            if getattr(dress_item, "object_id", "") == target_id:
                return dress_item
        return None
