# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    BanditCostumeItem = GameItem(
        object_id="dress_thiefdress",
        name="Костюм бандита",
        description="Костюм бандита состоит из вырвиглазных разноцветных желто-красно-синих-буромалиновых полосатых штанов и разноцветной шелковой рубашки, богато, но абсолютно безвкусно украшенной золотым шитьем. Это безвкусный, но достаточно дорогой костюм",
        price=1000,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "thiefdress",
            "wear_target": "player",
        },
    )
