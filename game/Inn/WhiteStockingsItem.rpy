init 4 python:
    WhiteStockingsItem = GameItem(
        object_id="dress_whitestockings",
        name="Белые чулки с поясом",
        description="Белые чулки из плотной ткани",
        price=150,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "whitestockings",
            "wear_target": "female",
        },
    )
