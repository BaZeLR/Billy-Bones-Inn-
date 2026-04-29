# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    PeasantCostumeItem = GameItem(
        object_id="dress_villagedress",
        name="Костюм деревенщины",
        description="Костюм деревенщины состоит из холщовых штанов, подпоясанных веревкой и рубахи из грубого полотна. Это самый простой и дешевый костюм",
        price=50,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "villagedress",
            "wear_target": "player",
        },
    )
