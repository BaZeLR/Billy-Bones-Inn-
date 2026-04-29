# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    BourgeoisCostumeItem = GameItem(
        object_id="dress_citydress",
        name="Костюм буржуа",
        description="Костюм буржуа состоит из черных штанов строгого покроя, кожаного ремня с серебрянной пряжкой и простого камзола с серебрянными пуговицами. Это простой, но не очень дешевый костюм",
        price=400,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "citydress",
            "wear_target": "player",
        },
    )
