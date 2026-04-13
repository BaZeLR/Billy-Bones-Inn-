init 4 python:
    SimplePantiesItem = GameItem(
        object_id="dress_simplepanties",
        name="Панталончики",
        description="Обычные панталончики",
        price=100,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "simplepanties",
            "wear_target": "female",
        },
    )
