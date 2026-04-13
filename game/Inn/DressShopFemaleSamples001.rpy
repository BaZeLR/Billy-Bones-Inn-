init python:
    DressShopFemaleSamplesObject = GameObject(
        object_id="female_samples_001",
        name="Женские образцы",
        description="Женские платья и прочие образцы одежды висят вдоль левой стены.",
        container=True,
        carriable=False,
        stackable=False,
        custom_properties={"rack_type": "female"},
    )
