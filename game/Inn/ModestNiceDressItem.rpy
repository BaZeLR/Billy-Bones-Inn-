init 4 python:
    ModestNiceDressItem = GameItem(
        object_id="dress_modestnicedress",
        name="Скромное выходное платье",
        description="Это в меру скромное нарядное платье. Белое, под цвет невинности, оттороченное кружевами, оно лишь немного открывает грудь. Подол же платья целомудренно спускается до пят",
        price=400,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "modestnicedress",
            "wear_target": "female",
        },
    )
