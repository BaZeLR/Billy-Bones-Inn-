init 4 python:
    CommUnitItem = GameItem(
        object_id="comm_unit_001",
        name="наручный коммуникатор",
        description="Наручный блок связи с откидным экраном и крошечной клавиатурой. Зелёная полоса сигнала едва светится.",
        picture="images/general/comm_unit_item.png",
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={"item_kind": "device", "wear_slot": "wrist", "source_thread": "tempestOpening"},
    )

    VibraniumRingItem = GameItem(
        object_id="vibranium_ring_001",
        name="вибраниумное кольцо",
        description="Тяжёлое кольцо из тёмного металла с голубым гранёным камнем и тонкими светящимися дорожками.",
        picture="images/general/vibranium_ring_item.png",
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={"item_kind": "device", "wear_slot": "finger", "source_thread": "tempestOpening"},
    )
