# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    SailorCostumeItem = GameItem(
        object_id="dress_sailordress",
        name="Костюм моряка",
        description="Костюм моряка состоит из не стесняющих движений просторных цветастых шаровар, удерживаемых поясом из бычей кожи, и богато, хотя и безвкусно вышитого жилета без рукавов, который обычно носят на голое тело. Это не очень дорогой костюм",
        price=300,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "sailordress",
            "wear_target": "player",
        },
    )
