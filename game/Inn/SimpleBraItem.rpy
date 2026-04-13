init 4 python:
    SimpleBraItem = GameItem(
        object_id="dress_simplebra",
        name="Лиф",
        description="Простой белый лиф",
        price=100,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "simplebra",
            "wear_target": "female",
        },
    )
