# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init 4 python:
    OpenWorkDressItem = GameItem(
        object_id="dress_openworkdress",
        name="Открытое рабочее платье",
        description="Это рабочее платье предназначенно для уверенных в себе дам. Не очень длинная коричневая юбка с белыми рюшечками не доходит до щиколоток, а легкая блузка с глубоким декольте оставляет открытыми руки и плечи, и позволяет всем желающим возможность заглянуть в привлекательную ложбинку",
        price=400,
        carriable=True,
        wearable=True,
        stackable=False,
        custom_properties={
            "item_kind": "wearable",
            "dress_code": "openworkdress",
            "wear_target": "female",
        },
    )
