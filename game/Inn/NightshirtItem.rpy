init 4 python:
    NightshirtItem = GameItem(
        object_id="dress_nightshirt",
        name="Ночная рубашка",
        description="Длинная, до пят, ночная рубашка из простой ткани",
        price=25,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "nightshirt",
            "wear_target": "female",
        },
    )
