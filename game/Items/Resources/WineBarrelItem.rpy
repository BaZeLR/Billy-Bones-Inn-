# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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
