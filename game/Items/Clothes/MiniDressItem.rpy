# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    MiniDressItem = GameItem(
        object_id="dress_minidress",
        name="Открытое платье",
        description="Этот сарафанчик безусловно привлечет внимание к его обладательнице. Короткая юбка доходит только до колен, а блузка из тонкой ткани без рукавов немногое оставляет воображению. Это платье для уверенной в себе девушки. Или, скорее, недевушки",
        price=500,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "minidress",
            "wear_target": "female",
        },
    )
