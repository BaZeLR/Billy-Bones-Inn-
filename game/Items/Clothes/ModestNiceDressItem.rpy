# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    ModestNiceDressItem = GameItem(
        object_id="dress_modestnicedress",
        name="Скромное выходное платье",
        description="Это в меру скромное нарядное платье. Белое, под цвет невинности, оттороченное кружевами, оно лишь немного открывает грудь. Подол же платья целомудренно спускается до пят",
        price=400,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "modestnicedress",
            "wear_target": "female",
        },
    )
