init 4 python:
    BlackStockingsItem = GameItem(
        object_id="dress_blackstockings",
        name="Черные чулки",
        description="Черные, кружевные, почти прозрачные чулки",
        price=200,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "blackstockings",
            "wear_target": "female",
        },
    )
