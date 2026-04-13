init 4 python:
    FoodBaleItem = GameItem(
        object_id="food_bale_001",
        name="провизия",
        description="Запас съестного для кухни трактира.",
        price=6,
        carriable=True,
        usable=True,
        stackable=True,
        custom_properties={
            "item_kind": "food",
            "supply_units": 10,
            "energy": 20,
            "fun": 5,
            "minutes": 30,
        },
    )
