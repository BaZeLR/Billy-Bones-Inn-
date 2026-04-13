init python:
    DressShopMaleSamplesObject = GameObject(
        object_id="male_samples_001",
        name="Мужские образцы",
        description="Мужские костюмы и камзолы развешаны вдоль правой стены.",
        container=True,
        carriable=False,
        stackable=False,
        custom_properties={"rack_type": "male"},
    )
