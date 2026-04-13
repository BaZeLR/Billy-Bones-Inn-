init 4 python:
    PeasantCostumeItem = GameItem(
        object_id="dress_villagedress",
        name="Костюм деревенщины",
        description="Костюм деревенщины состоит из холщовых штанов, подпоясанных веревкой и рубахи из грубого полотна. Это самый простой и дешевый костюм",
        price=50,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "villagedress",
            "wear_target": "player",
        },
    )
