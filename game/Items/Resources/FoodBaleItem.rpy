# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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
            "kitchen_depositable": True,
            "supply_units": 10,
            "energy": 20,
            "fun": 5,
            "minutes": 30,
        },
    )
