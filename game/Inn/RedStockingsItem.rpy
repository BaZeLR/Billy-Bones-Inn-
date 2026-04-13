init 4 python:
    RedStockingsItem = GameItem(
        object_id="dress_redstockings",
        name="Красные чулки с поясом",
        description="Красные, кружевные, почти прозрачные чулки",
        price=200,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "redstockings",
            "wear_target": "female",
        },
    )
