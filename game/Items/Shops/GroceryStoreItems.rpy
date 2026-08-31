# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    MilkPitcherItem = GameItem(
        object_id="milk_pitcher_001",
        name="крынка молока",
        description="Свежая крынка молока из утреннего надоя. Ее можно сразу пустить на общий стол или отдать на кухню.",
        price=6,
        carriable=True,
        stackable=True,
        custom_properties={
            "item_kind": "grocery_good",
            "grocery_kind": "milk",
            "kitchen_depositable": True,
        },
    )
