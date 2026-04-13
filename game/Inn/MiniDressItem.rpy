init 4 python:
    MiniDressItem = GameItem(
        object_id="dress_minidress",
        name="Открытое платье",
        description="Этот сарафанчик безусловно привлечет внимание к его обладательнице. Короткая юбка доходит только до колен, а блузка из тонкой ткани без рукавов немногое оставляет воображению. Это платье для уверенной в себе девушки. Или, скорее, недевушки",
        price=500,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "minidress",
            "wear_target": "female",
        },
    )
