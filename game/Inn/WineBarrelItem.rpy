init 4 python:
    WineBarrelItem = GameItem(
        object_id="wine_barrel_001",
        name="винная бочка",
        description="Большая дубовая бочка для хранения вина.",
        price=14,
        carriable=False,
        container=True,
        custom_properties={
            "item_kind": "container",
            "container_kind": "wine_barrel",
            "capacity_units": 10,
        },
    )
